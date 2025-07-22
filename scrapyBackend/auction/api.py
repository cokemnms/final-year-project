from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from .models import Auction, Bid,AuctionImage
from django.shortcuts import get_object_or_404
from .serializers import AuctionSerializer, BidSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_auction(request):
    data = request.data
    images = request.FILES.getlist('images')  # Get the list of images

    auction = Auction.objects.create(
        title=data['title'],
        description=data['description'],
        base_price=data['base_price'],
        created_by=request.user,
        expires_at=data.get('expires_at', None)
    )

    # Save multiple images
    for img in images:
        AuctionImage.objects.create(auction=auction, image=img)

    return Response(AuctionSerializer(auction, context={'request': request}).data)


@api_view(['GET'])
def list_auctions(request):
    auctions = Auction.objects.filter(is_active=True)
    serializer = AuctionSerializer(auctions, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def auction_detail(request, pk):
    auction = Auction.objects.get(pk=pk)
    return Response(AuctionSerializer(auction, context={'request': request}).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def place_bid(request, pk):
    auction = get_object_or_404(Auction, pk=pk)
    amount = request.data['amount']
    
    # Low bid warning
    if amount <= auction.base_price:
        return Response({
            'status': 'warning',
            'message': 'Your bid is below the base price. Please place a higher bid.'
        }, status=200)

    # Hard upper limit rule: no one can bid more than +5000 over base price
    if amount > auction.base_price + 5000:
        return Response({
            'status': 'warning',
            'message': 'Your bid is unusually high. Bids cannot exceed 5000 more than the current base price.'
        }, status=200)

    # Optional max_price rule (set by auction creator)
    if auction.max_price and amount > auction.max_price:
        return Response({
            'status': 'warning',
            'message': f'Bids cannot exceed the seller’s maximum allowed bid of ${auction.max_price}.'
        }, status=200)

    # Save bid
    bid = Bid.objects.create(
        auction=auction,
        bidder=request.user,
        amount=amount
    )
    # Optionally: update base_price to new bid
    auction.base_price = amount
    auction.save()

    return Response(BidSerializer(bid).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_auction(request, pk):
    auction = get_object_or_404(Auction, pk=pk, created_by=request.user)
    auction.is_active = False
    auction.save()
    return Response({'status': 'cancelled'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_auctions_by_user(request, user_id):
    auctions = Auction.objects.filter(created_by__id=user_id, is_active=True)
    serializer = AuctionSerializer(auctions, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_auction(request, pk):
    try:
        auction = Auction.objects.get(pk=pk)
    except Auction.DoesNotExist:
        return Response({'error': 'Auction not found'}, status=404)

    if auction.created_by != request.user:
        return Response({'error': 'Unauthorized'}, status=403)

    auction.delete()
    return Response({'message': 'Auction deleted successfully'}, status=204)