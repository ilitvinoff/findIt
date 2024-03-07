from django import forms

from announcement.models import Announcement, AnnouncementImage, Category


class AnnouncementCreateForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      error_messages={"required": "Please select the category"})

    class Meta:
        model = Announcement
        fields = ["category", "title", "content", "poster", "price"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 5}),
        }


AnnouncementImageCreateFormsSetFactory = forms.inlineformset_factory(Announcement, AnnouncementImage, fields=["file"],
                                                                     max_num=10, absolute_max=20, extra=0)
