from django import forms
from . models import Temario, Prueba, Formado_por

class TemarioForm(forms.ModelForm):
    
    class Meta:
        model = Temario
        fields = ['NomTemario','IdOposicion','Archivo']

class ExamenForm(forms.Form):
    def __init__(self, *args, **kwargs):
        preguntas = kwargs.pop('preguntas', None) 
        super(ExamenForm, self).__init__(*args, **kwargs)
  
        for pregunta in preguntas:
            opciones = [(opcion, opcion) for opcion in pregunta['opciones']]
            self.fields[f'pregunta_{pregunta["id"]}'] = forms.ChoiceField(label=pregunta['texto'], choices=opciones, widget=forms.RadioSelect(), required=False)

        
    def evaluar_respuestas(self, preguntas):
        puntaje = 0
        incorrectas = 0
        blanco = 0
        nota = 0
        acertadas = []
        falladas = []
        blancas = []
        respuestas = []
        respuestas_usuario = self.cleaned_data
        for pregunta in preguntas:
            nombre_campo = f'pregunta_{pregunta["id"]}'
            respuesta_usuario = respuestas_usuario.get(nombre_campo)
            respuestas.append((pregunta["id"],respuesta_usuario))
            if respuesta_usuario == pregunta['respuesta_correcta']:
                puntaje += 1
                nota += 1
                acertadas.append(pregunta["id"])
            elif  respuesta_usuario == '':
                blanco += 1
                blancas.append(pregunta["id"])
            else:
                incorrectas += 1
                nota -= 0.25
                falladas.append(pregunta["id"])

        if nota > 0:
            nota = (nota / (puntaje+blanco+incorrectas)) * 10
        else:
            nota = 0
            
        return puntaje, incorrectas, blanco, nota, acertadas, falladas, blancas, respuestas
    
class PruebaForm(forms.ModelForm):
    temarios = forms.ModelMultipleChoiceField(queryset=Temario.objects.all())
    class Meta:
        model = Prueba
        fields = ['NomPrueba', 'temarios','NumPreguntas']


    
