from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from models import Block

class BlocksViewSet(viewsets.ModelViewSet):

    queryset = Block.objects.all()

    def create(self, request):
        obj = Block.createBlock(request.data['blockType'])
        return Response(obj.id)

    @detail_route(methods=['post'])
    def remove(self, request, pk=None):
        obj = Block.objects.get(pk=pk)
        block = obj.getBlock()
        slot = request.data['slot']
        block.remove(int(slot))
        obj.saveBlock(block)
        return Response('SUCCESS')

    @detail_route(methods=['post'])
    def add(self, request, pk=None):
        obj = Block.objects.get(pk=pk)
        block = obj.getBlock()
        slot = None
        if 'slot' in request.data:
            slot = request.data['slot']
        toAdd = request.data['toAdd']
        if not block._isInput:
            toAdd = Block.objects.get(pk=toAdd).getBlock()
            addType = block.getInputType(slot)
            # Check that block type matches up
            if (toAdd.getOutputType() != addType):
                return Response('FAILURE')
        if slot is None:
            block.add(toAdd)
        else:
            block.add(toAdd, int(slot))
        obj.saveBlock(block)
        return Response('SUCCESS')


    @detail_route(methods=['get'])
    def evaluate(self, request, pk=None):
        block = Block.objects.get(pk=pk).getBlock()
        result = block.evaluate()
        return Response(result)

    @detail_route(methods=['get'])
    def collapse(self, request, pk=None):
        block = self.get_object().getBlock()
        newBlock = block.collapse()
        newObj = Block.collapseBlock(newBlock)
        return Response(newObj.id)
