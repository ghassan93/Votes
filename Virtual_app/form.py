from django import forms



class VirtualElectionForm(forms.Form):
    
    name = forms.CharField(max_length = 200)
    ssn = forms.IntegerField()
    answer = forms.CharField()
