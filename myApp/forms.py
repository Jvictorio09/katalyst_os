from django import forms

TONE_CHOICES = [
    ("professional","Professional"),
    ("friendly","Friendly"),
    ("persuasive","Persuasive"),
    ("informative","Informative"),
    ("casual","Casual"),
]
LENGTH_CHOICES = [
    ("short","Short (200–300 words)"),
    ("medium","Medium (500–800 words)"),
    ("long","Long (1000+ words)"),
]
TYPE_CHOICES = [
    ("blog","Blog Post"),
    ("article","Article"),
    ("marketing","Marketing Copy"),
    ("product","Product Description"),
    ("social","Social Media Post"),
    ("newsletter","Email Newsletter"),
    ("press","Press Release"),
]

class ContentRequestForm(forms.Form):
    content_type = forms.ChoiceField(choices=TYPE_CHOICES)
    topic = forms.CharField(max_length=200)
    audience = forms.CharField(max_length=200, required=False)
    key_points = forms.CharField(widget=forms.Textarea, required=False)
    tone = forms.ChoiceField(choices=TONE_CHOICES)
    length = forms.ChoiceField(choices=LENGTH_CHOICES)
