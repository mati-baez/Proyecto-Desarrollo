from django import forms


class CiudadForm(forms.Form):
    ciudad = forms.CharField(
        label="Ciudad",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            "placeholder": "Ej: Buenos Aires",
            "class": "form-control",
        }),
    )

    def clean_ciudad(self):
        value = (self.cleaned_data.get("ciudad") or "").strip()
        if not value:
            raise forms.ValidationError("Ingresá una ciudad.")
        return value

