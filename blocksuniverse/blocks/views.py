from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from models import Block

class BlocksViewSet(viewsets.ModelViewSet):

    queryset = Block.objects.all()
    
    @detail_route(methods=['post'])
    def add(self, request, pk=None):
        obj = Block.objects.get(pk=pk)
        block = obj.getBlock()
        toAdd = request.data['toAdd']
        if not block._isInput:
            toAdd = Block.objects.get(pk=toAdd).getBlock()
        block.add(toAdd)
        obj.saveBlock(block)
        return Response('SUCCESS')
        

    @detail_route(methods=['get'])
    def evaluate(self, request, pk=None):
        block = self.get_object().getBlock()
        result = block.evaluate()
        return Response(result)

    @detail_route(methods=['get'])
    def collapse(self, request, pk=None):
        block = self.get_object().getBlock()
        newBlock = block.collapse()
        newObj = Block.collapseBlock(newBlock)
        return Response(newObj.id)
    
    def create(self, request):
        obj = Block.createBlock(request.data['blockType'])
        return Response(obj.id)

# Create your views here.
