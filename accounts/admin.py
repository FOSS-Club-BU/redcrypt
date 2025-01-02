from django.contrib import admin
from accounts.models import Profile, IPs, contact_form
from accounts.utils import generate_avatar


class IPsAdmin(admin.ModelAdmin):
    readonly_fields = ('ip_address',)
    list_filter = ('count',)
    list_display = [
        'ip_address',
        'count']
    fields = [
        ('users_from_ip', 'count'),
        ('ip_address',)
    ]


class ProfileAdmin(admin.ModelAdmin):
    search_fields = ['user__username', 'name', 'discord_id']
    readonly_fields = ('user', 'last_completed_time')
    list_display = [
        'user',
        'score',
        'current_level',
        'ip_address_count'
    ]
    list_filter = ['is_banned', 'ip_address_count', 'current_level']
    fieldsets = (
        ('Details',
            {'fields': [
                ('user'),
                ('name', 'is_public_name'),
                ('organization', 'is_public_organization'),
                ('discord_id'),
                ('avatar_url')
                ]}),
        ('Hunt',
            {'fields': [
                ('score', 'current_level'),
                ('last_completed_time'),
                ('banned_reason', 'is_banned'),
                ('rank', 'stats')
                ]}),
        ('IPs',
            {'fields': [
                ('ip_address', 'ip_address_count')
                ]})
    )

    def reset_profile_pic(self, request, queryset):
        for profile in queryset:
            avatar_path = generate_avatar(profile.user.username)
            profile.avatar.name = avatar_path
            profile.save()
        self.message_user(request, "Updated avatars")

    reset_profile_pic.short_description = "Reset Avatar"
    actions=[reset_profile_pic]


class contact_formAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'subject',
        'body'
    ]
    fields = [
        ('user'),
        ('subject'),
        ('body')
    ]


admin.site.register(Profile, ProfileAdmin)
admin.site.register(IPs, IPsAdmin)
admin.site.register(contact_form, contact_formAdmin)
