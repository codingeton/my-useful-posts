from django import forms
from blog.models import Post, Comment, LeveragePercentage
from django.contrib.auth.forms import AuthenticationForm

class PostForm(forms.ModelForm):

    class Meta():
        model = Post #Connecting the model to Post model
        fields = ('author','title','text')

        #create widgets (dictionary attributes)for fields for styling them using custom classes in css
        widgets = {
            'title': forms.TextInput(attrs={'class':'textinputclass'}),
            'text': forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})
        }

class CommentForm(forms.ModelForm):

    class Meta():
        model = Comment #Connecting the model to the comment model
        fields = ('author','text',)

        #Create widgets similar to that of PostForm

        widgets = {
            'author': forms.TextInput(attrs={'class':'textinputclass'}),
            'text': forms.Textarea(attrs={'class':'editable medium-editor-textarea'})
        }

class LeveragePercentageForm(forms.ModelForm):

    class Meta():
        model = LeveragePercentage
        fields = ('name','source','reference')
