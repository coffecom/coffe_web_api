from rest_framework import serializers
from .models import Item, DaySchedule, Receipt, ReceiptItem

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class DayScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DaySchedule
        fields = '__all__'

    def to_representation(self, obj):
        ret = super(DayScheduleSerializer, self).to_representation(obj)
        ret['emploee_before_12_1'] = obj.emploee_before_12_1.username
        ret['emploee_before_12_2'] = obj.emploee_before_12_2.username

        ret['emploee_after_12_1'] = obj.emploee_after_12_1.username
        ret['emploee_after_12_2'] = obj.emploee_after_12_2.username

        # ret['creator'] = obj.creator.username

        
class ReceiptItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceiptItem
        fields = '__all__'


    def to_representation(self, obj):
        ret = super(ReceiptItemSerializer, self).to_representation(obj)
        ret['item'] = obj.item.name + " with cost:" + str(obj.item.cost)
        return ret 
        
    def __str__(self):
        return f"{self.quantity} of {self.item}"

class ReceiptSerializer(serializers.ModelSerializer):
    items = serializers.StringRelatedField(many = True)

    class Meta:
        model = Receipt
        fields = '__all__'

    def to_representation(self, obj):
        ret = super(ReceiptSerializer, self).to_representation(obj)
        ret['creator'] = obj.creator.username

        return ret 
