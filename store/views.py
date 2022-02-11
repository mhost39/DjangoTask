
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.generics import get_object_or_404

from django.core.mail import send_mail

from .models import Organization
from .serializers import DNASerializer, OrderSerializer
from .permissions import IsAdmin
from .models import DNA, Order


def validate_gene_sequence(gene_sequence):
        c = gene_sequence.lower().count('c')
        g = gene_sequence.lower().count('g')
        ratio = (c + g) / len(gene_sequence) * 100
        if ratio < 25.0 or ratio > 65.0:
            return "invalid"
        return "valid"


class DNAViewSet(ModelViewSet):
    permission_classes=[IsAuthenticated, IsAdmin]

    queryset = DNA.objects.all()
    serializer_class = DNASerializer

    def create(self, request, *args, **kwargs):
        data = request.data.get('genes')
        result = []
        for row in data:
            stat = validate_gene_sequence(row['gene'])
            if stat == "valid":
                serializer = DNASerializer(data={"gene_sequence": row['gene'], "organization":row['organization']})
                # import ipdb; ipdb.set_trace()
                if serializer.is_valid():
                    serializer.save()
            result.append(stat)
        
        return Response(
                {
                    "details": "DNAs Added Successfully",
                    "data": result,
                    "valid_gene_sequences": result.count("valid"),
                    "invalid_gene_sequences": result.count("invalid"),
                },
                status=status.HTTP_201_CREATED
            )


class OrderViewSet(ModelViewSet):
    permission_classes=[IsAuthenticated]

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        customer = request.user

        dna = DNA.objects.filter(id=request.data.get("dna")).first()
        # dna = DNA.objects.get_object_or_404(request.data.get("dna"))

        if customer.organization == dna.organization:
            return Response(
                {
                    "details": "Sorry you can order DNA from your organization.",
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = OrderSerializer(data={"dna": dna.id, "customer": customer.id})
        if serializer.is_valid():
                    serializer.save()
        
        return Response(
                {
                    "details": "Order created Successfully and in review",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED
            )


    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAdmin])
    def me(self, request, id=None):
        
        order = Order.objects.get(id=request.data.get('id'))
        if request.method == 'GET':
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        elif request.method == 'PUT':
            request.data['customer'] = order.customer.id
            serializer = OrderSerializer(order, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            send_mail(
                subject="DNA Order",
                message="your order has been verified you can check now",
                from_email='mhost39@gmail.com',
                recipient_list=[order.customer.email ],
            )
            return Response(serializer.data)
