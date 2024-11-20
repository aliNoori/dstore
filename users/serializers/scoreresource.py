from rest_framework import serializers

from users.models.score import Score

class ScoreResource(serializers.ModelSerializer):

    created_at=serializers.SerializerMethodField()
    
        
   
    class Meta:
        model = Score
        fields = ['id', 'score', 'reason', 'date_added','created_at','description'] 


    def get_created_at(self, obj):
              
        return obj.date_added     