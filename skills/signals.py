from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Skill, Goal, Notification

@receiver(post_save, sender=Goal)
def goal_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.user,
            message = f"📝 New goal added: '{instance.goal}'"
            )
    elif instance.is_completed:
        Notification.objects.create(
            user = instance.user,
            message = f"🎉 Goal completed: '{instance.goal}'"
        )

@receiver(post_save, sender=Skill)
def skill_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.user,
            message = f"🚀 New Skill added: '{instance.name}'"
        )
        
