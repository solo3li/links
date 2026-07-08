from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe
from .models import Profile, Link

class ColorWidget(forms.TextInput):
    def render(self, name, value, attrs=None, renderer=None):
        text_html = super().render(name, value, attrs, renderer)
        # HTML5 color picker requires a 7-character hex code (e.g., #ffffff)
        color_val = value if value and str(value).startswith('#') and len(value) == 7 else "#ffffff"
        input_id = attrs.get('id', f'id_{name}') if attrs else f'id_{name}'
        
        color_picker = f'''
        <input type="color" id="{input_id}_colorpicker" value="{color_val}" 
               oninput="document.getElementById('{input_id}').value = this.value"
               style="vertical-align: middle; margin-right: 5px; height: 28px; width: 30px; border: none; cursor: pointer; padding: 0; background: none;">
        '''
        return mark_safe(f'<div style="display: inline-flex; align-items: center;">{text_html}{color_picker}</div>')

class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = '__all__'
        widgets = {
            'bg_color': ColorWidget(),
            'text_color': ColorWidget(),
        }

class LinkInline(admin.TabularInline):
    model = Link
    form = LinkForm
    extra = 1
    fields = ('title', 'url', 'icon_platform', 'icon_class', 'bg_color', 'text_color', 'order', 'is_active', 'is_highlighted')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [LinkInline]

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    form = LinkForm
    list_display = ('title', 'url', 'icon_platform', 'bg_color', 'text_color', 'order', 'is_active', 'is_highlighted')
    list_editable = ('icon_platform', 'bg_color', 'text_color', 'order', 'is_active', 'is_highlighted')
    list_filter = ('is_active', 'is_highlighted')
    search_fields = ('title', 'url')

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name in ['bg_color', 'text_color']:
            kwargs['widget'] = ColorWidget()
        return super().formfield_for_dbfield(db_field, request, **kwargs)
