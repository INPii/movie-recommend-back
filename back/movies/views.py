from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.db.models import Q
from rest_framework import status
from django.shortcuts import get_object_or_404,get_list_or_404
from .models import Genre, Movie, People, Keyword,Review
from .serializers.genre import GenreSerializer,GenreDetailSerializer
from .serializers.people import PeopleListSerializer, PeopleDetailSerializer
from .serializers.movie import MovieListSerializer, MovieDetailSerializer
from .serializers.keyword import KeywordSerializer, KeywordDetailSerializer
from .serializers.searchmovie import MovieSerializer
from .serializers.review import ReviewListSerializer,ReviewDetailSerializer,ReviewCreateSerializer
from accounts.serializers import ProfileSerializer,ProfileListSerializer
from accounts.models import User
# from django.contrib.auth import get_user_model

# User = get_user_model()
# 모든 view함수 뒤에 ALL이 붙으면 전체를 response, List가 붙으면 start를 기준으로 10개씩 보내도록 
@api_view(['GET'])
def genreAll(request):
    genres = Genre.objects.all()
    serializer = GenreSerializer(genres, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def genreList(request, start):
    genres = Genre.objects.all()
    response = genres[start:start+10]
    serializer = GenreSerializer(response, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def genreDetail(request, genre_id):
    genre = get_object_or_404(Genre, pk=genre_id)
    serializer = GenreDetailSerializer(genre)
    return Response(serializer.data)

@api_view(['GET'])
def actorAll(request):
    actors = People.objects.filter(known_for_department='Acting')
    serializer = PeopleListSerializer(actors, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def actorList(request,start):
    actors = People.objects.filter(known_for_department='Acting')
    response = actors[start:start+10]
    serializer = PeopleListSerializer(response, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def directorAll(request):
    directors = People.objects.filter(known_for_department='Directing')
    serializer = PeopleListSerializer(directors, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def directorList(request,start):
    directors = People.objects.filter(known_for_department='Directing')
    response = directors[start:start+10]
    serializer = PeopleListSerializer(response, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def directorList(request, start):
    directors = People.objects.filter(known_for_department='Directing')
    response = directors[start: start + 10]
    serializer = PeopleListSerializer(response, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def actorDetail(request, actor_id):
    actor = get_object_or_404(People, known_for_department='Acting', pk=actor_id)
    serializer = PeopleDetailSerializer(actor)
    return Response(serializer.data)

@api_view(['GET'])
def directorDetail(request, director_id):
    director = get_object_or_404(People, known_for_department='Directing', pk=director_id)
    serializer = PeopleDetailSerializer(director)
    return Response(serializer.data)

@api_view(['GET'])
def keywordAll(request):
    keywords = Keyword.objects.all()
    serializer = KeywordSerializer(keywords, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def keywordList(request,start):
    keywords = Keyword.objects.all()
    response = keywords[start:start+10]
    serializer = KeywordSerializer(response, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def keywordDetail(request, keyword_id):
    keyword = get_object_or_404(Keyword,  pk=keyword_id)
    serializer = KeywordDetailSerializer(keyword)
    return Response(serializer.data)

@api_view(['GET'])
def boxOffice(request):
    movies = Movie.objects.all().order_by('-popularity')[:10]
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def movieAll(request):
    user = request.user
    movies = Movie.objects.all()
    serializer = MovieListSerializer(movies, many=True)
    
    refine_list = []
    print(user)
    if user.is_authenticated:
        for movie in serializer.data:
            movie_id = movie['id']
            is_liked = user.like_movie.filter(id=movie_id).exists()  # 사용자가 좋아요를 눌렀는지 확인
            movie['is_liked'] = is_liked  # True 또는 False로 결과를 추가
            refine_list.append(movie)
        response_data = refine_list
        
    else:
        response_data =serializer.data
    
    return Response(response_data)
@api_view(['GET'])
def movieList(request, start):
    movies = Movie.objects.all()
    reponse = movies[start: start+10]
    serializer = MovieListSerializer(reponse, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def movieDetail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    serializer = MovieDetailSerializer(movie)
    return Response(serializer.data)



def search_movies(query):
    query_terms = query.split()
    filters = Q()

    for term in query_terms:
        
        term_filter = (
            Q(title__icontains=term) |
            Q(original_title__icontains=term) |
            Q(overview__icontains=term) |
            Q(genres__name__icontains=term) |
            Q(people__name__icontains=term) |
            Q(keyword__name__icontains=term)
        )
        filters &= term_filter

    movies = Movie.objects.filter(filters).distinct()
   
    def sort_key(movie):
        title_matches = any(term.lower() in movie.title.lower() for term in query_terms)
        keyword_matches = any(term.lower() in [kw.name.lower() for kw in movie.keyword.all()] for term in query_terms)
        overview_matches = any(term.lower() in movie.overview.lower() for term in query_terms)
        genre_matches = any(term.lower() in [genre.name.lower() for genre in movie.genres.all()] for term in query_terms)
        people_matches = any(term.lower() in [person.name.lower() for person in movie.people.all()] for term in query_terms)
        
        return (
            not title_matches,
            not keyword_matches,
            not overview_matches,
            not genre_matches,
            not people_matches,
        )

    sorted_movies = sorted(movies, key=sort_key)
    
    return sorted_movies

@api_view(['GET'])
def search_movies_view(request):
    query = request.GET.get('q')
    
    if not query:
        return Response({"message": "검색어를 입력해주세요."}, status=400)
    
    
    movies = search_movies(query)
    if not movies:
        return Response({"message": "검색결과가 없습니다."}, status=404)
    
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def reviewAll(request):
    reviews = get_list_or_404(Review)
    serializer = ReviewListSerializer(reviews, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def reviewList(request,start):
    reviews = get_list_or_404(Review)
    response = reviews[start:start+10]
    serializer = ReviewListSerializer(response, many=True)
    return Response(serializer.data)



@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def review(request, movie_id):
    
    if request.method == 'GET':
        reviews = Review.objects.filter(movie_id=movie_id)
        serializer = ReviewDetailSerializer(reviews, many=True)
        return Response(serializer.data)
        
    elif request.method == 'POST':
        movie = get_object_or_404(Movie, pk=movie_id)
        existing_review = Review.objects.filter(movie=movie, user=request.user).first()
        if existing_review:
            if request.user.nickname:
                return Response({"message": f"{request.user.nickname}님의 리뷰가 이미 존재합니다. 리뷰 수정만 가능합니다."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": f"리뷰가 이미 존재합니다. 리뷰 수정만 가능합니다."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ReviewCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, movie=movie)
            movie.update_vote_average() # 평점 업데이트
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def reviewDetail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if request.method == 'GET':
        serializer = ReviewDetailSerializer(review)
        return Response(serializer.data)
    elif request.method == 'PUT':
        if request.user != review.user:
            return Response({"detail":"리뷰 작성자만 리뷰를 수정할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)
        serializer = ReviewDetailSerializer(review,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            review.movie.update_vote_average() #평점 업데이트
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        if request.user != review.user:
            return Response({"detail":"리뷰 작성자만 리뷰를 삭제할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)
    
    review.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
        

#자기자신 프로필
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    user = get_object_or_404(User, pk=request.user.id)
    serializer = ProfileSerializer(instance=user)
    return Response(serializer.data)

#다른 사람 프로필 페이지
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profileDetail(request,user_id):
    user = get_object_or_404(User, pk=user_id)
    serializer = ProfileSerializer(instance=user)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profileList(request):
    users = User.objects.filter(is_superuser=False).filter(is_staff=False)
    serializer = ProfileListSerializer(instance=users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_movie(request,movie_id):
    user=request.user
    movie = get_object_or_404(Movie, pk=movie_id)
    if movie.like_user.filter(pk=user.pk).exists():
        movie.like_user.remove(user)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    else:
        movie.like_user.add(user)
        serializer = MovieSerializer(movie)
        return Response(serializer.data) 
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def review_like(request, review_id):
    user=request.user
    review = get_object_or_404(Movie, pk=review_id)
    if review.like_user.filter(pk=user.pk).exists():
        review.like_user.remove(user)
        serializer = ReviewDetailSerializer(review)
        return Response(serializer.data)
    else:
        review.like_user.add(user)
        serializer = ReviewDetailSerializer(review)
        return Response(serializer.data) 
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow(request, user_id):
    user = request.user
    target_user = get_object_or_404(User, id=user_id)

    if user == target_user:
        return Response({"error": "자기자신을 팔로우 할수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

    if target_user.followers.filter(id=user.id).exists():
        target_user.followers.remove(user)
        return Response({"status": "언팔로우"}, status=status.HTTP_200_OK)
    else:
        target_user.followers.add(user)
        return Response({"status": "팔로우"}, status=status.HTTP_200_OK)
