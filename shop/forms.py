from django import forms
from .models import Product, Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price', 'image', 'opt_price', 'id_1c'] 
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название товара'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите описание товара',
                'rows': 4
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
                'id': 'category-select'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '1',
                'min': '0'
            }),
            'opt_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '1',
                'min': '0'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'id': 'image-upload'
            }),
            'id_1c': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'ID в 1С',
                'step': '1',
                'min': '0'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Заполняем категории из базы данных
        self.fields['category'].queryset = Category.objects.all().order_by('name')
        # Делаем поле категории обязательным
        self.fields['category'].required = True