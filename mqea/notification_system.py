"""
Система уведомлений для MQEA.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

import asyncio
import smtplib
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable, Any, Union
from dataclasses import dataclass, asdict
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading
from enum import Enum
import uuid

from .realtime_monitoring import MonitoringAlert, AlertLevel


class NotificationChannel(Enum):
    """Каналы уведомлений."""
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    WEBHOOK = "webhook"
    CONSOLE = "console"
    LOG = "log"


class NotificationPriority(Enum):
    """Приоритет уведомления."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class NotificationTemplate:
    """Шаблон уведомления."""
    template_id: str
    name: str
    channel: NotificationChannel
    subject_template: str
    body_template: str
    priority: NotificationPriority = NotificationPriority.MEDIUM
    enabled: bool = True
    
    def render(self, alert: MonitoringAlert, patient_name: str = "Пациент") -> tuple:
        """Рендерит шаблон с данными."""
        context = {
            'patient_name': patient_name,
            'patient_id': alert.patient_id,
            'sensor_id': alert.sensor_id,
            'alert_level': alert.alert_level.value,
            'value': alert.value,
            'threshold': alert.threshold,
            'message': alert.message,
            'timestamp': alert.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            'alert_id': alert.alert_id
        }
        
        subject = self.subject_template.format(**context)
        body = self.body_template.format(**context)
        
        return subject, body


@dataclass
class NotificationRule:
    """Правило уведомлений."""
    rule_id: str
    name: str
    conditions: Dict[str, Any]  # условия срабатывания
    templates: List[str]  # ID шаблонов
    cooldown_minutes: int = 5  # время между уведомлениями
    enabled: bool = True
    last_triggered: Optional[datetime] = None


@dataclass
class NotificationRecord:
    """Запись об отправленном уведомлении."""
    notification_id: str
    rule_id: str
    template_id: str
    channel: NotificationChannel
    recipient: str
    subject: str
    body: str
    priority: NotificationPriority
    status: str  # sent, failed, pending
    timestamp: datetime
    error_message: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Преобразует в словарь."""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        data['channel'] = self.channel.value
        data['priority'] = self.priority.value
        return data


class NotificationChannelHandler:
    """Базовый класс обработчика канала уведомлений."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.enabled = True
    
    async def send_notification(self, recipient: str, subject: str, body: str, 
                              priority: NotificationPriority) -> bool:
        """Отправляет уведомление."""
        raise NotImplementedError


class ConsoleNotificationHandler(NotificationChannelHandler):
    """Обработчик консольных уведомлений."""
    
    async def send_notification(self, recipient: str, subject: str, body: str, 
                              priority: NotificationPriority) -> bool:
        """Отправляет уведомление в консоль."""
        priority_emoji = {
            NotificationPriority.LOW: "ℹ️",
            NotificationPriority.MEDIUM: "⚠️",
            NotificationPriority.HIGH: "🔴",
            NotificationPriority.CRITICAL: "🚨"
        }
        
        emoji = priority_emoji.get(priority, "📢")
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        print(f"\n{emoji} УВЕДОМЛЕНИЕ [{timestamp}]")
        print(f"   Получатель: {recipient}")
        print(f"   Тема: {subject}")
        print(f"   Приоритет: {priority.value}")
        print(f"   Сообщение: {body}")
        print("-" * 50)
        
        return True


class EmailNotificationHandler(NotificationChannelHandler):
    """Обработчик email уведомлений."""
    
    async def send_notification(self, recipient: str, subject: str, body: str, 
                              priority: NotificationPriority) -> bool:
        """Отправляет email уведомление."""
        try:
            smtp_server = self.config.get('smtp_server', 'localhost')
            smtp_port = self.config.get('smtp_port', 587)
            username = self.config.get('username', '')
            password = self.config.get('password', '')
            from_email = self.config.get('from_email', username)
            
            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = recipient
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # Отправка email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                if username and password:
                    server.login(username, password)
                server.send_message(msg)
            
            return True
            
        except Exception as e:
            print(f"Ошибка отправки email: {e}")
            return False


class WebhookNotificationHandler(NotificationChannelHandler):
    """Обработчик webhook уведомлений."""
    
    async def send_notification(self, recipient: str, subject: str, body: str, 
                              priority: NotificationPriority) -> bool:
        """Отправляет webhook уведомление."""
        try:
            import aiohttp
            
            webhook_url = recipient
            headers = self.config.get('headers', {'Content-Type': 'application/json'})
            
            payload = {
                'subject': subject,
                'body': body,
                'priority': priority.value,
                'timestamp': datetime.now().isoformat()
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(webhook_url, json=payload, headers=headers) as response:
                    return response.status == 200
                    
        except Exception as e:
            print(f"Ошибка отправки webhook: {e}")
            return False


class LogNotificationHandler(NotificationChannelHandler):
    """Обработчик уведомлений в лог."""
    
    async def send_notification(self, recipient: str, subject: str, body: str, 
                              priority: NotificationPriority) -> bool:
        """Записывает уведомление в лог."""
        try:
            log_file = self.config.get('log_file', 'notifications.log')
            timestamp = datetime.now().isoformat()
            
            log_entry = {
                'timestamp': timestamp,
                'recipient': recipient,
                'subject': subject,
                'body': body,
                'priority': priority.value
            }
            
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
            
            return True
            
        except Exception as e:
            print(f"Ошибка записи в лог: {e}")
            return False


class NotificationSystem:
    """Система уведомлений."""
    
    def __init__(self):
        self.templates: Dict[str, NotificationTemplate] = {}
        self.rules: Dict[str, NotificationRule] = {}
        self.handlers: Dict[NotificationChannel, NotificationChannelHandler] = {}
        self.notification_history: List[NotificationRecord] = []
        self.recipients: Dict[str, Dict[str, str]] = {}  # recipient_id -> {email, phone, etc.}
        
        # Инициализируем обработчики по умолчанию
        self._initialize_default_handlers()
        self._create_default_templates()
        self._create_default_rules()
    
    def _initialize_default_handlers(self):
        """Инициализирует обработчики по умолчанию."""
        self.handlers[NotificationChannel.CONSOLE] = ConsoleNotificationHandler({})
        self.handlers[NotificationChannel.LOG] = LogNotificationHandler({'log_file': 'mqea_notifications.log'})
        
        # Email обработчик (требует настройки)
        email_config = {
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'username': '',
            'password': '',
            'from_email': 'mqea@hospital.com'
        }
        self.handlers[NotificationChannel.EMAIL] = EmailNotificationHandler(email_config)
        
        # Webhook обработчик
        self.handlers[NotificationChannel.WEBHOOK] = WebhookNotificationHandler({})
    
    def _create_default_templates(self):
        """Создает шаблоны по умолчанию."""
        templates = [
            NotificationTemplate(
                template_id="critical_alert_email",
                name="Критическая тревога (Email)",
                channel=NotificationChannel.EMAIL,
                subject_template="🚨 КРИТИЧЕСКАЯ ТРЕВОГА - {patient_name}",
                body_template="""Критическая медицинская тревога!

Пациент: {patient_name} (ID: {patient_id})
Время: {timestamp}
Датчик: {sensor_id}
Уровень тревоги: {alert_level}
Значение: {value}
Сообщение: {message}

Пожалуйста, немедленно проверьте состояние пациента.

ID тревоги: {alert_id}
""",
                priority=NotificationPriority.CRITICAL
            ),
            NotificationTemplate(
                template_id="warning_alert_console",
                name="Предупреждение (Консоль)",
                channel=NotificationChannel.CONSOLE,
                subject_template="⚠️ Предупреждение - {patient_name}",
                body_template="Предупреждение: {message}\nПациент: {patient_name}\nВремя: {timestamp}",
                priority=NotificationPriority.MEDIUM
            ),
            NotificationTemplate(
                template_id="emergency_alert_all",
                name="Экстренная тревога (Все каналы)",
                channel=NotificationChannel.CONSOLE,
                subject_template="🚨 ЭКСТРЕННАЯ ТРЕВОГА - {patient_name}",
                body_template="""🚨 ЭКСТРЕННАЯ МЕДИЦИНСКАЯ ТРЕВОГА! 🚨

Пациент: {patient_name} (ID: {patient_id})
Время: {timestamp}
Датчик: {sensor_id}
Значение: {value}
Сообщение: {message}

ТРЕБУЕТСЯ НЕМЕДЛЕННОЕ ВМЕШАТЕЛЬСТВО!

ID тревоги: {alert_id}
""",
                priority=NotificationPriority.CRITICAL
            ),
            NotificationTemplate(
                template_id="alert_log",
                name="Логирование тревог",
                channel=NotificationChannel.LOG,
                subject_template="Alert: {alert_level} - {patient_name}",
                body_template="Alert ID: {alert_id}\nPatient: {patient_name}\nSensor: {sensor_id}\nValue: {value}\nMessage: {message}\nTimestamp: {timestamp}",
                priority=NotificationPriority.LOW
            )
        ]
        
        for template in templates:
            self.templates[template.template_id] = template
    
    def _create_default_rules(self):
        """Создает правила по умолчанию."""
        rules = [
            NotificationRule(
                rule_id="critical_alerts",
                name="Критические тревоги",
                conditions={
                    'alert_level': AlertLevel.CRITICAL.value,
                    'channels': ['email', 'console', 'log']
                },
                templates=["critical_alert_email", "warning_alert_console", "alert_log"],
                cooldown_minutes=2
            ),
            NotificationRule(
                rule_id="emergency_alerts",
                name="Экстренные тревоги",
                conditions={
                    'alert_level': AlertLevel.EMERGENCY.value,
                    'channels': ['email', 'console', 'log', 'webhook']
                },
                templates=["emergency_alert_all", "alert_log"],
                cooldown_minutes=0
            ),
            NotificationRule(
                rule_id="warning_alerts",
                name="Предупреждения",
                conditions={
                    'alert_level': AlertLevel.WARNING.value,
                    'channels': ['console', 'log']
                },
                templates=["warning_alert_console", "alert_log"],
                cooldown_minutes=10
            )
        ]
        
        for rule in rules:
            self.rules[rule.rule_id] = rule
    
    def add_recipient(self, recipient_id: str, **contact_info):
        """Добавляет получателя уведомлений."""
        self.recipients[recipient_id] = contact_info
        print(f"📧 Получатель {recipient_id} добавлен")
    
    def add_template(self, template: NotificationTemplate):
        """Добавляет шаблон."""
        self.templates[template.template_id] = template
        print(f"📝 Шаблон {template.name} добавлен")
    
    def add_rule(self, rule: NotificationRule):
        """Добавляет правило."""
        self.rules[rule.rule_id] = rule
        print(f"📋 Правило {rule.name} добавлено")
    
    def _should_send_notification(self, rule: NotificationRule) -> bool:
        """Проверяет, нужно ли отправлять уведомление (cooldown)."""
        if not rule.enabled:
            return False
        
        if rule.last_triggered is None:
            return True
        
        time_since_last = datetime.now() - rule.last_triggered
        return time_since_last.total_seconds() >= (rule.cooldown_minutes * 60)
    
    def _get_recipients_for_channel(self, channel: NotificationChannel) -> List[str]:
        """Получает список получателей для канала."""
        recipients = []
        for recipient_id, contact_info in self.recipients.items():
            if channel == NotificationChannel.EMAIL and 'email' in contact_info:
                recipients.append(contact_info['email'])
            elif channel == NotificationChannel.SMS and 'phone' in contact_info:
                recipients.append(contact_info['phone'])
            elif channel == NotificationChannel.WEBHOOK and 'webhook' in contact_info:
                recipients.append(contact_info['webhook'])
        
        return recipients
    
    async def process_alert(self, alert: MonitoringAlert, patient_name: str = "Пациент"):
        """Обрабатывает тревогу и отправляет уведомления."""
        print(f"🔔 Обработка тревоги: {alert.alert_level.value} - {alert.sensor_id}")
        
        # Находим подходящие правила
        matching_rules = []
        for rule in self.rules.values():
            if self._should_send_notification(rule):
                # Проверяем условия
                if rule.conditions.get('alert_level') == alert.alert_level.value:
                    matching_rules.append(rule)
        
        # Отправляем уведомления по правилам
        for rule in matching_rules:
            await self._send_notifications_for_rule(rule, alert, patient_name)
            rule.last_triggered = datetime.now()
    
    async def _send_notifications_for_rule(self, rule: NotificationRule, alert: MonitoringAlert, 
                                         patient_name: str):
        """Отправляет уведомления по правилу."""
        for template_id in rule.templates:
            if template_id in self.templates:
                template = self.templates[template_id]
                await self._send_notification_template(template, alert, patient_name)
    
    async def _send_notification_template(self, template: NotificationTemplate, alert: MonitoringAlert, 
                                        patient_name: str):
        """Отправляет уведомление по шаблону."""
        if not template.enabled:
            return
        
        # Рендерим шаблон
        subject, body = template.render(alert, patient_name)
        
        # Получаем получателей
        recipients = self._get_recipients_for_channel(template.channel)
        
        # Если нет получателей, используем дефолтных
        if not recipients:
            if template.channel == NotificationChannel.CONSOLE:
                recipients = ["console"]
            elif template.channel == NotificationChannel.LOG:
                recipients = ["log"]
        
        # Отправляем каждому получателю
        for recipient in recipients:
            await self._send_single_notification(
                template, recipient, subject, body, alert
            )
    
    async def _send_single_notification(self, template: NotificationTemplate, recipient: str,
                                      subject: str, body: str, alert: MonitoringAlert):
        """Отправляет одно уведомление."""
        handler = self.handlers.get(template.channel)
        if not handler:
            print(f"⚠️ Обработчик для канала {template.channel.value} не найден")
            return
        
        notification_id = str(uuid.uuid4())
        start_time = datetime.now()
        
        try:
            success = await handler.send_notification(
                recipient, subject, body, template.priority
            )
            
            status = "sent" if success else "failed"
            error_message = None if success else "Ошибка отправки"
            
        except Exception as e:
            status = "failed"
            error_message = str(e)
            success = False
        
        # Записываем в историю
        record = NotificationRecord(
            notification_id=notification_id,
            rule_id="",  # TODO: добавить отслеживание правила
            template_id=template.template_id,
            channel=template.channel,
            recipient=recipient,
            subject=subject,
            body=body,
            priority=template.priority,
            status=status,
            timestamp=start_time,
            error_message=error_message
        )
        
        self.notification_history.append(record)
        
        if success:
            print(f"✅ Уведомление отправлено: {template.channel.value} -> {recipient}")
        else:
            print(f"❌ Ошибка отправки: {template.channel.value} -> {recipient}: {error_message}")
    
    def get_notification_history(self, limit: int = 50) -> List[Dict]:
        """Получает историю уведомлений."""
        recent = self.notification_history[-limit:] if self.notification_history else []
        return [record.to_dict() for record in recent]
    
    def get_statistics(self) -> Dict:
        """Получает статистику уведомлений."""
        total = len(self.notification_history)
        sent = len([r for r in self.notification_history if r.status == "sent"])
        failed = len([r for r in self.notification_history if r.status == "failed"])
        
        # Статистика по каналам
        channel_stats = {}
        for record in self.notification_history:
            channel = record.channel.value
            if channel not in channel_stats:
                channel_stats[channel] = {'sent': 0, 'failed': 0}
            channel_stats[channel][record.status] += 1
        
        return {
            'total_notifications': total,
            'sent_notifications': sent,
            'failed_notifications': failed,
            'success_rate': (sent / total * 100) if total > 0 else 0,
            'channel_statistics': channel_stats,
            'active_templates': len([t for t in self.templates.values() if t.enabled]),
            'active_rules': len([r for r in self.rules.values() if r.enabled]),
            'total_recipients': len(self.recipients)
        }


# Функции для создания и управления системой
def create_notification_system() -> NotificationSystem:
    """Создает систему уведомлений."""
    return NotificationSystem()


async def demo_notification_system():
    """Демонстрация системы уведомлений."""
    print("🔔 MQEA - Демонстрация системы уведомлений")
    print("=" * 50)
    
    # Создаем систему уведомлений
    notification_system = create_notification_system()
    
    # Добавляем тестовых получателей
    notification_system.add_recipient(
        "doctor1",
        email="doctor1@hospital.com",
        phone="+992123456789"
    )
    notification_system.add_recipient(
        "nurse1", 
        email="nurse1@hospital.com",
        phone="+992123456790"
    )
    
    # Создаем тестовые тревоги
    from .realtime_monitoring import MonitoringAlert
    
    test_alerts = [
        MonitoringAlert(
            alert_id="test1",
            sensor_id="heart_rate",
            patient_id="P001",
            alert_level=AlertLevel.WARNING,
            message="Высокая частота сердечных сокращений",
            timestamp=datetime.now(),
            value=110.0,
            threshold=(100, 120)
        ),
        MonitoringAlert(
            alert_id="test2",
            sensor_id="oxygen_saturation",
            patient_id="P002",
            alert_level=AlertLevel.CRITICAL,
            message="Низкое насыщение кислородом",
            timestamp=datetime.now(),
            value=88.0,
            threshold=(85, 95)
        ),
        MonitoringAlert(
            alert_id="test3",
            sensor_id="temperature",
            patient_id="P003",
            alert_level=AlertLevel.EMERGENCY,
            message="Критически высокая температура",
            timestamp=datetime.now(),
            value=39.5,
            threshold=(38.5, 40.0)
        )
    ]
    
    print("\n📧 Отправка тестовых уведомлений...")
    
    # Обрабатываем тревоги
    for alert in test_alerts:
        patient_names = {
            "P001": "Али Хасанов",
            "P002": "Фатима Алимова", 
            "P003": "Ахмад Рахимов"
        }
        patient_name = patient_names.get(alert.patient_id, "Неизвестный пациент")
        
        await notification_system.process_alert(alert, patient_name)
        await asyncio.sleep(1)  # небольшая пауза между уведомлениями
    
    # Показываем статистику
    print("\n📊 Статистика уведомлений:")
    stats = notification_system.get_statistics()
    print(f"   Всего отправлено: {stats['total_notifications']}")
    print(f"   Успешно: {stats['sent_notifications']}")
    print(f"   Ошибок: {stats['failed_notifications']}")
    print(f"   Успешность: {stats['success_rate']:.1f}%")
    
    print(f"\n📈 По каналам:")
    for channel, channel_stats in stats['channel_statistics'].items():
        print(f"   {channel}: {channel_stats['sent']} отправлено, {channel_stats['failed']} ошибок")
    
    print("\n✅ Демонстрация завершена")


if __name__ == "__main__":
    asyncio.run(demo_notification_system())

