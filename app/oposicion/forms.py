from django import forms
from . models import Temario

class TemarioForm(forms.ModelForm):
    
    class Meta:
        model = Temario
        fields = ['NomTemario','IdOposicion','Archivo']

class ExamenForm(forms.Form):
    def __init__(self, *args, **kwargs):
        preguntas = kwargs.pop('preguntas', None)  # Aseguramos que preguntas no sea None
        super(ExamenForm, self).__init__(*args, **kwargs)
  
        for pregunta in preguntas:
            opciones = [(opcion, opcion) for opcion in pregunta['opciones']]
            self.fields[f'pregunta_{pregunta["id"]}'] = forms.ChoiceField(label=pregunta['texto'], choices=opciones, widget=forms.RadioSelect(), required=False)

        
    def evaluar_respuestas(self, preguntas):
        puntaje = 0
        incorrectas = 0
        blanco = 0
        respuestas_usuario = self.cleaned_data
        for pregunta in preguntas:
            nombre_campo = f'pregunta_{pregunta["id"]}'
            respuesta_usuario = respuestas_usuario.get(nombre_campo)
            if respuesta_usuario == pregunta['respuesta_correcta']:
                puntaje += 1
            elif  respuesta_usuario == '':
                blanco += 1
            else:
                incorrectas += 1
        return puntaje, incorrectas, blanco