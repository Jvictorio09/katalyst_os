from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from myApp.models import Tool, Project, Activity

class Command(BaseCommand):
    help = "Seed demo data for Katalyst OS dashboard"

    def handle(self, *args, **kwargs):
        User = get_user_model()
        
        # Get or create a demo user
        user, created = User.objects.get_or_create(
            username="demo@katalyst.local",
            defaults={
                "email": "demo@katalyst.local",
                "is_staff": True,
                "is_superuser": True
            }
        )
        if created:
            user.set_password("demo12345")
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Created demo user: {user.username}"))
        else:
            self.stdout.write(self.style.WARNING(f"User already exists: {user.username}"))

        # Create tools
        tools_data = [
            ("Email Copilot", "AI-powered email writing and management assistant.", "email"),
            ("Image Generator", "Create stunning images from text descriptions.", "image"),
            ("Video Generator", "Generate professional videos with AI assistance.", "video"),
            ("Code Assistant", "AI-powered coding help and code generation.", "code"),
            ("Content Writer", "Generate blog posts, articles, and marketing copy.", "content"),
            ("Analytics", "Track and analyze your AI tool usage and performance.", "analytics"),
        ]
        
        for name, desc, icon in tools_data:
            tool, created = Tool.objects.get_or_create(
                name=name,
                owner=user,
                defaults={"description": desc, "icon": icon, "is_active": True}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"[+] Created tool: {name}"))

        # Create projects
        projects_data = [
            "Katalyst Site Revamp",
            "NeuroMed AI Pilot",
            "Lioraè Co. Landing",
        ]
        
        for name in projects_data:
            project, created = Project.objects.get_or_create(
                name=name,
                owner=user,
                defaults={"status": "active"}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"[+] Created project: {name}"))

        # Create activities
        activities_data = [
            ("email", "Email drafted with AI"),
            ("image", "Generated 5 product images"),
            ("video", "Created marketing video"),
            ("content", "Published 'Luxury Landscaping Trends' article"),
            ("analytics", "Weekly performance report exported"),
            ("code", "Generated API endpoints"),
            ("email", "Sent newsletter to 1,000 subscribers"),
            ("image", "Created social media graphics"),
            ("video", "Edited tutorial video"),
            ("content", "Wrote product description"),
        ]
        
        # Only create activities if none exist for this user
        if not Activity.objects.filter(user=user).exists():
            for kind, text in activities_data:
                Activity.objects.create(user=user, kind=kind, text=text)
                self.stdout.write(self.style.SUCCESS(f"[+] Created activity: {text}"))
        else:
            self.stdout.write(self.style.WARNING("Activities already exist for this user"))

        self.stdout.write(
            self.style.SUCCESS(
                "\n[SUCCESS] Seeding complete! Login credentials:\n"
                "Username: demo@katalyst.local\n"
                "Password: demo12345"
            )
        )

