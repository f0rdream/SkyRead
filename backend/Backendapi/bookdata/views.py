# coding:utf-8
import time

from django.db.models import Q
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
)

from library.permissions import have_phone_register
from .models import Book,Refer,Holding,StarBook, ReadPlan
from .serializers import (BookInfoSerializer,
                          ShortInto,
                          SearchSerializer,
                          HoldingSerializer,
                          StarBookSerializer,
                          StarBookDetailSerializer,
                          PostCommentSerializer,
                          PostReadPlanSerializer,
                          CommentDetailSerializer,
                          ReadPlanDetailSerializer)
from rest_framework.views import APIView
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_201_CREATED,
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_403_FORBIDDEN)
from rest_framework.response import Response
from history.models import SearchHistory
from l_lib.function import get_reply
from models import Comment
class BookInfoView(APIView):
    serializer_class = BookInfoSerializer
    permission_classes = [AllowAny]
    # authentication_classes = [SessionAuthentication]
    def get(self,request,isbn13):
        isbn13 = str(isbn13)
        try:
            book = Book.objects.get(isbn13=isbn13)
        except:
            return Response({'error': 'can not find this book'}, HTTP_404_NOT_FOUND)
        serializer = BookInfoSerializer(book,data=request.data)
        serializer.is_valid(raise_exception=True)
        response = Response(serializer.data, HTTP_200_OK)
        return response


class Serach(APIView):
    permission_classes = [AllowAny]

    def get(self,request):
        key = self.request.GET.get("key")
        # 存入搜索历史
        try:
            queryset = SearchHistory.objects.filter(user=request.user,key=key)
            if len(queryset) >= 1:
                pass
            else:
                s = SearchHistory.objects.create(user=request.user,key=key)
                s.save()
        except Exception as e:
            print e
        if key:
            title_queryset = Book.objects.filter(Q(title__icontains=key) |
                                                 Q(subtitle__icontains=key))
            author_queryset = Book.objects.filter(Q(author__icontains=key))
            title_serializer = ShortInto(title_queryset,data=request.data,many=True)
            title_serializer.is_valid(raise_exception=True)
            author_serializer = ShortInto(author_queryset,data=request.data,many=True)
            author_serializer.is_valid(raise_exception=True)
            reply = dict()
            reply['title_result'] = title_serializer.data
            reply['author_result'] = author_serializer.data
            return Response(reply,HTTP_200_OK)
        else:
            reply = {'msg':'None'}
            return Response(reply,HTTP_200_OK)


class ReferBookView(APIView):
    """
    相关书籍
    """
    permission_classes = [AllowAny]

    def get(self,request,isbn13):
        try:
            r = Refer.objects.get(isbn13=isbn13)
            refer_id = r.refer_id
            refer_object_list = list()
            refer = refer_id.split("&")
            for i in range(1, len(refer)):
                try:
                    b = Book.objects.get(d_id=refer[i])
                    refer_object_list.append(b)
                except:
                    pass
            serializer = ShortInto(refer_object_list, data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data,HTTP_200_OK)
        except:
            reply = get_reply(91,"not found")
            return Response(reply,HTTP_404_NOT_FOUND)


class HoldingView(APIView):
    """
    馆藏信息VIEW
    """
    permission_classes = [AllowAny]

    def get(self,request,isbn13):
        try:
           queryset = Holding.objects.filter(isbn13=isbn13)
           if not queryset:
               reply = get_reply(92, "not found")
               return Response(reply, HTTP_404_NOT_FOUND)
           serializer = HoldingSerializer(queryset,data=request.data,many=True)
           serializer.is_valid(raise_exception=True)
           return Response(serializer.data,HTTP_200_OK)
        except Exception as e:
            reply = get_reply(92,"not found")
            return Response(reply,HTTP_404_NOT_FOUND)


class StarBookView(APIView):
    """
    我的收藏书籍
    """
    permission_classes = [IsAuthenticated]
    serializer_class = StarBookSerializer

    def post(self,request):
        serializer = StarBookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        isbn13 = serializer.validated_data['isbn13']
        try:
            book = Book.objects.get(isbn13=isbn13)
            user = request.user
            # 判断这本书是否已经存在
            try:
                before_book = StarBook.objects.get(user=user,book=book)
                return Response(get_reply(98, 'fail'))
            except:
                pass
            starbook = StarBook.objects.create(user=user,book=book)
            starbook.save()
            return Response(get_reply(0,'success'))
        except:
            return Response(get_reply(98,'fail'))

    def get(self,request):
        user = request.user
        queryset = StarBook.objects.filter(user=user)
        # book_list = list()
        # for starbook in queryset:
        #     book = starbook.book
        #     book_list.append(book)
        serializer = StarBookDetailSerializer(queryset,data=request.data,many=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data,HTTP_200_OK)


class GuideBookView(APIView):
    """
    书籍导航
    """
    permission_classes =  [IsAuthenticated]

    def get(self,request,guide_id,page):
        if page < 1:
            return Response(get_reply(81,'error page'),HTTP_404_NOT_FOUND)
        begin_page = (int(page)-1)*20
        end_page = begin_page+20
        try:
            queryset = Book.guide_objects.get_guide_book(int(guide_id))[begin_page:end_page]
            serializer = ShortInto(queryset,many=True,data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data,HTTP_200_OK)
        except Exception as e:
            return Response(get_reply(0,e),HTTP_404_NOT_FOUND)


class StarBookDetailView(APIView):
    """
    收藏书籍详情

    """
    permission_classes = [IsAuthenticated]
    def get(self,request,pk):
        if not have_phone_register(user=request.user):
            reply = get_reply(17,'not register with phone')
            return Response(reply,HTTP_403_FORBIDDEN)
        user = request.user
        try:
            star_item = StarBook.objects.get(user=user,pk=pk)

            serializer = StarBookDetailSerializer(star_item,data=request.data)
            serializer.is_valid(raise_exception=True)
            response = Response(serializer.data,HTTP_200_OK)
            return response
        except StarBook.DoesNotExist:
            reply = get_reply(82,'item not found')
            response = Response(reply,HTTP_404_NOT_FOUND)
            return response

    def delete(self,request,pk):
        if not have_phone_register(user=request.user):
            reply = get_reply(17,'not register with phone')
            return Response(reply,HTTP_403_FORBIDDEN)
        user = request.user
        try:
            star_item = StarBook.objects.get(user=user, pk=pk)
            serializer = StarBookDetailSerializer(star_item, data=request.data)
            serializer.is_valid(raise_exception=True)
            try:
                star_item.delete()
                reply = get_reply(0,'success')
                response = Response(reply,HTTP_200_OK)
                return response
            except:
                content = get_reply(83,'delete fail')
                response = Response(content, HTTP_400_BAD_REQUEST)
                return response
        except StarBook.DoesNotExist:
            content = get_reply(82,'item not found')
            response = Response(content, HTTP_404_NOT_FOUND)
            return response


class CommentView(APIView):
    """
    查看或者发表评论
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PostCommentSerializer

    def post(self,request,isbn13):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        content = serializer.validated_data['content']
        comment = Comment.objects.create(isbn13=isbn13,
                                         content=content,
                                         user=user)
        comment.save()
        return Response(serializer.data,HTTP_200_OK)
    def get(self,request,isbn13):
        queryset = Comment.objects.filter(isbn13=isbn13)
        serializer = CommentDetailSerializer(queryset,many=True,data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data,HTTP_200_OK)


class ReadPlanView(APIView):
    """
    阅读计划详情
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PostReadPlanSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        isbn13 = serializer.validated_data['isbn13']
        begin_time = serializer.validated_data['begin_time']
        end_time = serializer.validated_data['end_time']
        readplan = ReadPlan.objects.create(
            user=user,
            isbn13=isbn13,
            begin_time=begin_time,
            end_time=end_time
        )
        readplan.save()
        return Response(get_reply(0,'success'),HTTP_201_CREATED)

    def get(self,request):
        queryset = ReadPlan.objects.filter(user=request.user)
        serializer = ReadPlanDetailSerializer(queryset,data=request.data,many=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data,HTTP_200_OK)


class ReadPlanDetailView(APIView):
    """
    删除阅读计划
    """
    permission_classes = [IsAuthenticated]

    def delete(self,request,pk):
        if not have_phone_register(user=request.user):
            reply = get_reply(17,'not register with phone')
            return Response(reply,HTTP_403_FORBIDDEN)
        user = request.user
        try:
            plan_item = ReadPlan.objects.get(user=user, pk=pk)
            try:
                plan_item.delete()
                reply = get_reply(0,'success')
                response = Response(reply,HTTP_200_OK)
                return response
            except:
                content = get_reply(115,'delete fail')
                response = Response(content, HTTP_400_BAD_REQUEST)
                return response
        except StarBook.DoesNotExist:
            content = get_reply(116,'item not found')
            response = Response(content, HTTP_404_NOT_FOUND)
            return response
