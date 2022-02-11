from rest_framework import serializers
from .models import DNA, Order


class DNASerializer(serializers.ModelSerializer):
    
    class Meta:  
        model = DNA
        fields = ('gene_sequence', 'id', 'organization')

class ChoicesSerializerField(serializers.SerializerMethodField):

    def to_representation(self, value):
        method_name = 'get_{field_name}_display'.format(field_name=self.field_name)
        method = getattr(value, method_name)
        return method()

class OrderSerializer(serializers.ModelSerializer):
    #status = ChoicesSerializerField()
    class Meta:  
        model = Order
        fields = ('dna', 'ordered_at', 'customer', 'price', 'status')
