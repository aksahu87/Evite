from django import forms


MY_CHOICES = (
    ('1','IFT530'),
    ('2','IFT540'),
)

class EventForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'size':135,'placeholder': 'Enter a title for the event'}))
    date = forms.DateField(widget = forms.SelectDateWidget())
    time = forms.TimeField(widget=forms.TimeInput(format='%H:%M',attrs={'size':135,'placeholder':'HH:MM Format'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'size':135,'placeholder': 'Enter a description for the event'}))
    maxinvites = forms.IntegerField(widget=forms.NumberInput(attrs={'size':135,'placeholder': 'Max no Invitees'}))
    maxGuests = forms.IntegerField(widget=forms.NumberInput(attrs={'size':135,'placeholder': 'Max no Guests'}))
    location = forms.CharField(widget=forms.TextInput(attrs={'size':135,'placeholder': 'Location of the event'}))
    clubname = forms.ChoiceField(choices=MY_CHOICES)
    
class RSVPForm(forms.Form):
     Coming_to_party = forms.CharField(max_length=1)
     no_of_guests = forms.IntegerField()

     def clean_Coming_to_party(self):
         cd = self.cleaned_data['Coming_to_party']
         if cd not in ['Y','N']:
             raise forms.ValidationError("Enter Y/N only")
         return cd
              
     def clean_no_of_guests(self):
         cd = self.cleaned_data['no_of_guests']
         if cd > 5:
             string = "only "+str(5)+" guests are allowed"
             raise forms.ValidationError(string)
         return cd 
         
class FEEDBACKForm(forms.Form):
     comment = forms.CharField( widget=forms.Textarea )
     rating = forms.IntegerField(label="Rating (Enter from 1 to 5, 5 being highest)")

     def clean_rating(self):
         cd = self.cleaned_data['rating']
         if cd not in (1,2,3,4,5):
             string = "Enter proper value"
             raise forms.ValidationError(string)
         return cd 