from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from models import Block

class BlocksViewSet(viewsets.ViewSet):

    queryset = Block.objects.all()
    
    @detail_route(methods=['post'])
    def add(self, request, toAdd=None, pk=None):
        obj = self.get_object()
        block = obj.getBlock()
        toAdd = Block.objects.get(toAdd).getBlock()
        block.add(toAdd)
        obj.saveBlock(block)
        return Response('SUCCESS')
        

    @detail_route(methods=['get'])
    def evaluate(self, request, pk=None):
        block = self.get_object().getBlock()
        result = block.evaluate()
        return Response(result)

    def create(self, request, blockType=None):
        obj = Block.objects.createBlock(blockType)
        return Response('SUCCESS')

# Create your views here.
