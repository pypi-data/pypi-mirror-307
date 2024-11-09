from aadiscordbot.tasks import send_message

from django.contrib.auth.models import User
from django.db import transaction
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from allianceauth.services.hooks import get_extension_logger

# from discord import Color, Embed


logger = get_extension_logger(__name__)
# logger = logging.getLogger(__name__)


@receiver(m2m_changed, sender=User.groups.through)
def m2m_changed_user_groups(sender, instance: User, action, pk_set, *args, **kwargs):
    logger.debug(
        f"ASMEK Received m2m_changed from {instance} groups with action {action}"
    )

    def trigger_welcome_message():
        try:
            logger.debug("Sending welcome message %s" % instance)
            # find the groups!
            users_groups = instance.groups.filter(
                pk__in=pk_set, groupwelcome__isnull=False
            )
            logger.debug(users_groups)
            for g in users_groups:
                if g.id in pk_set:
                    # joined a group that has a welcome message!
                    group_msg = g.groupwelcome
                    # send welcome message in channel
                    channel = group_msg.channel  # channel to send message in
                    msg = group_msg.message  # welcome message
                    name = g.name  # group name
                    udid = instance.discord.uid  # discord ID of user
                    """e = Embed(
                        description=msg,
                        color=Color.yellow(),
                    )"""
                    pmsg = f"**Welcome to {name}** <@{udid}>\n {msg}"
                    send_message(channel_id=channel, message=pmsg)  # Message

        except Exception as err:
            logger.error(err)
            pass  # shits fucked... Don't worry about it...

    if instance.pk and (action == "post_add"):
        logger.debug("Waiting for commit to send message! %s" % instance)
        transaction.on_commit(trigger_welcome_message)
