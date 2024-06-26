import discord

ACTION_NAMES = {
    discord.AuditLogAction.guild_update: "Server Updates",
    discord.AuditLogAction.channel_update: "Channel Logs",
    discord.AuditLogAction.channel_create: "Channel Logs",
    discord.AuditLogAction.channel_delete: "Channel Logs",
    discord.AuditLogAction.overwrite_create: "Overwrite Logs",
    discord.AuditLogAction.overwrite_update: "Overwrite Logs",
    discord.AuditLogAction.overwrite_delete: "Overwrite Logs",
    discord.AuditLogAction.member_update: "Member Logs",
    discord.AuditLogAction.member_role_update: "Member Logs",
    discord.AuditLogAction.member_move: "Member Logs",
    discord.AuditLogAction.member_disconnect: "Member Logs",
    discord.AuditLogAction.member_prune: "Member Logs",
    discord.AuditLogAction.kick: "Member Management",
    discord.AuditLogAction.ban: "Member Management",
    discord.AuditLogAction.unban: "Member Management",
    discord.AuditLogAction.bot_add: "Bot Logs",
    discord.AuditLogAction.message_delete: "Message Logs",
    discord.AuditLogAction.message_bulk_delete: "Message Logs",
    discord.AuditLogAction.message_pin: "Message Logs",
    discord.AuditLogAction.message_unpin: "Message Logs",
    discord.AuditLogAction.integration_create: "Integration Logs",
    discord.AuditLogAction.integration_update: "Integration Logs",
    discord.AuditLogAction.integration_delete: "Integration Logs",
    discord.AuditLogAction.stage_instance_create: "Stage Logs",
    discord.AuditLogAction.stage_instance_update: "Stage Logs",
    discord.AuditLogAction.stage_instance_delete: "Stage Logs",
    discord.AuditLogAction.role_create: "Role Logs",
    discord.AuditLogAction.role_update: "Role Logs",
    discord.AuditLogAction.role_delete: "Role Logs",
    discord.AuditLogAction.invite_create: "Invite Logs",
    discord.AuditLogAction.invite_delete: "Invite Logs",
    discord.AuditLogAction.webhook_create: "Webhook Logs",
    discord.AuditLogAction.webhook_update: "Webhook Logs",
    discord.AuditLogAction.webhook_delete: "Webhook Logs",
    discord.AuditLogAction.emoji_create: "Emoji Logs",
    discord.AuditLogAction.emoji_update: "Emoji Logs",
    discord.AuditLogAction.emoji_delete: "Emoji Logs",
    discord.AuditLogAction.sticker_create: "Sticker Logs",
    discord.AuditLogAction.sticker_update: "Sticker Logs",
    discord.AuditLogAction.sticker_delete: "Sticker Logs",
    discord.AuditLogAction.thread_create: "Thread Logs",
    discord.AuditLogAction.thread_update: "Thread Logs",
    discord.AuditLogAction.thread_delete: "Thread Logs",
    discord.AuditLogAction.automod_rule_create: "Automod Logs",
    discord.AuditLogAction.automod_rule_update: "Automod Logs",
    discord.AuditLogAction.automod_rule_delete: "Automod Logs",
}

ACTION_EMOJIS = {
    discord.AuditLogAction.guild_update: discord.PartialEmoji.from_str("<:log_guild_update:1080533975153508352>"),
    discord.AuditLogAction.channel_update: discord.PartialEmoji.from_str("<:log_all:1080194735932711042>"),
    discord.AuditLogAction.channel_create: discord.PartialEmoji.from_str("<:log_all:1080194735932711042>"),
    discord.AuditLogAction.channel_delete: discord.PartialEmoji.from_str("<:log_all:1080194735932711042>"),
    discord.AuditLogAction.overwrite_create: discord.PartialEmoji.from_str("<:log_all:1080194735932711042>"),
    discord.AuditLogAction.overwrite_update: discord.PartialEmoji.from_str("<:log_all:1080194735932711042>"),
    discord.AuditLogAction.overwrite_delete: discord.PartialEmoji.from_str("<:log_all:1080194735932711042>"),
    discord.AuditLogAction.member_update: discord.PartialEmoji.from_str("<:log_member_update:1080194421229899829>"),
    discord.AuditLogAction.member_role_update: discord.PartialEmoji.from_str("<:log_member_update:1080194421229899829>"),
    discord.AuditLogAction.member_move: discord.PartialEmoji.from_str("<:log_member_update:1080194421229899829>"),
    discord.AuditLogAction.member_disconnect: discord.PartialEmoji.from_str("<:log_member_update:1080194421229899829>"),
    discord.AuditLogAction.bot_add: discord.PartialEmoji.from_str("<:log_member_plus:1112472154181750865>"),
    discord.AuditLogAction.message_delete: discord.PartialEmoji.from_str("<:log_msg_minus:1112333427249795123>"),
    discord.AuditLogAction.message_bulk_delete: discord.PartialEmoji.from_str("<:log_msg_minus:1112333427249795123>"),
    discord.AuditLogAction.message_pin: discord.PartialEmoji.from_str("<:log_msg_update:1112333368332402699>"),
    discord.AuditLogAction.message_unpin: discord.PartialEmoji.from_str("<:log_msg_update:1112333368332402699>"),
    discord.AuditLogAction.kick: discord.PartialEmoji.from_str("<:log_member_minus:1112472097323745300>"),
    discord.AuditLogAction.ban: discord.PartialEmoji.from_str("<:log_member_minus:1112472097323745300>"),
    discord.AuditLogAction.unban: discord.PartialEmoji.from_str("<:log_member_plus:1112472154181750865>"),
    discord.AuditLogAction.stage_instance_create: discord.PartialEmoji.from_str(
        "<:log_stage_instance_plus:1112333263348965497>",
    ),
    discord.AuditLogAction.stage_instance_update: discord.PartialEmoji.from_str(
        "<:log_stage_instance_update:1112332826369589319>",
    ),
    discord.AuditLogAction.stage_instance_delete: discord.PartialEmoji.from_str(
        "<:log_stage_instance_minus:1112332874939637810>",
    ),
    discord.AuditLogAction.integration_create: discord.PartialEmoji.from_str("<:log_integration_plus:1080195469503905793>"),
    discord.AuditLogAction.integration_update: discord.PartialEmoji.from_str(
        "<:log_integration_update:1080194889536516207>",
    ),
    discord.AuditLogAction.integration_delete: discord.PartialEmoji.from_str("<:log_integration_minus:1080530500806000640>"),
    discord.AuditLogAction.role_create: discord.PartialEmoji.from_str("<:log_role_plus:1080529743591518228>"),
    discord.AuditLogAction.role_update: discord.PartialEmoji.from_str("<:log_role_update:1080529964169965608>"),
    discord.AuditLogAction.role_delete: discord.PartialEmoji.from_str("<:log_role_minus:1080529853851369534>"),
    discord.AuditLogAction.invite_create: discord.PartialEmoji.from_str("<:log_invite_plus:1080194590088368248>"),
    discord.AuditLogAction.invite_delete: discord.PartialEmoji.from_str("<:log_invite_minus:1080530325760905346>"),
    discord.AuditLogAction.webhook_create: discord.PartialEmoji.from_str("<:log_integration_plus:1080195469503905793>"),
    discord.AuditLogAction.webhook_update: discord.PartialEmoji.from_str("<:log_integration_update:1080194889536516207>"),
    discord.AuditLogAction.webhook_delete: discord.PartialEmoji.from_str("<:log_integration_minus:1080530500806000640>"),
    discord.AuditLogAction.emoji_create: discord.PartialEmoji.from_str("<:log_emoji_plus:1080530759087042610>"),
    discord.AuditLogAction.emoji_update: discord.PartialEmoji.from_str("<:log_emoji_update:1080194953453518909>"),
    discord.AuditLogAction.emoji_delete: discord.PartialEmoji.from_str("<:log_emoji_minus:1080195415602888786>"),
    discord.AuditLogAction.sticker_create: discord.PartialEmoji.from_str("<:log_sticker_plus:1080530914024620084>"),
    discord.AuditLogAction.sticker_update: discord.PartialEmoji.from_str("<:log_sticker_update:1080531003250065478>"),
    discord.AuditLogAction.sticker_delete: discord.PartialEmoji.from_str("<:log_sticker_minus:1080530961776775229>"),
    discord.AuditLogAction.thread_create: discord.PartialEmoji.from_str("<:log_thread_plus:1080531262424502353>"),
    discord.AuditLogAction.thread_update: discord.PartialEmoji.from_str("<:log_thread_update:1080531355978449007>"),
    discord.AuditLogAction.thread_delete: discord.PartialEmoji.from_str("<:log_thread_minus:1080531308947718164>"),
    discord.AuditLogAction.automod_rule_create: discord.PartialEmoji.from_str("<:log_automod_plus:1080194794795585626>"),
    discord.AuditLogAction.automod_rule_update: discord.PartialEmoji.from_str("<:log_automod_update:1080194841989890048>"),
    discord.AuditLogAction.automod_rule_delete: discord.PartialEmoji.from_str("<:log_automod_minus:1080194682442743858>"),
}
