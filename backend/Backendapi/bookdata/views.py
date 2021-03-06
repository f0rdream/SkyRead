# coding:utf-8
import time
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
)
from library.permissions import have_phone_register
from .models import Book,Refer,Holding,StarBook, ReadPlan, ImageFile
from .serializers import (BookInfoSerializer,
                          ShortInto,
                          SearchSerializer,
                          HoldingSerializer,
                          StarBookSerializer,
                          StarBookDetailSerializer,
                          PostCommentSerializer,
                          PostReadPlanSerializer,
                          CommentDetailSerializer,
                          ReadPlanDetailSerializer,
                          Img2TextSerializer,
                          NotePostSerializer,
                          NoteGetSerializer,
                          RecordPostSerializer,RecordGetSerializer)
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
from models import Comment, BrowsedBook, Note, PlanRecord
from function import entry, book_price, image_to_text
from library.models import BorrowItem
from refer_spider import refer_book


class BookInfoView(APIView):
    serializer_class = BookInfoSerializer
    permission_classes = [AllowAny]
    # authentication_classes = [SessionAuthentication]
    def get(self,request,isbn13):
        user=request.user
        isbn13 = str(isbn13)
        try:
            book = Book.objects.get(isbn13=isbn13)
        except:
            return Response({'error': 'can not find this book'}, HTTP_404_NOT_FOUND)
        serializer = BookInfoSerializer(book,data=request.data)
        serializer.is_valid(raise_exception=True)
        # 查看是否收藏
        reply = serializer.data
        try:
            star_book = StarBook.objects.get(user=request.user,book=book)
            reply['stared'] = True
        except:
            reply['stared'] = False
        # 存入用户兴趣的isbn13
        try:
            queryset = BrowsedBook.objects.filter(user=user,isbn13=isbn13)
            if len(queryset) >= 1:
                pass
            else:
                b = BrowsedBook.objects.create(user=request.user,isbn13=isbn13)
                b.save()
        except Exception as e:
            print e
            pass

        response = Response(reply, HTTP_200_OK)
        return response


class Serach(APIView):
    """
    图书搜索
    """
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
        # 6.24日暂时只是返回标题模糊搜索结果
        if key:
            begin = time.time()
            from django.db import connection
            cursor = connection.cursor()
            text_index = ''
            for i in key:
                sql = "select number from bookinfo.char_number where title='%s'" % i
                cursor.execute(sql)
                rs = cursor.fetchall()
                for row in rs:
                    number = row[0]
                    text_index += '&'
                    text_index += number
            select_sql = "select isbn13 from bookdata_book where match (title_for_index)\
              against ('+%s' in boolean mode) order by average desc limit 15;" % text_index
            cursor.execute(select_sql)
            title_rs = cursor.fetchall()
            isbn13_list = []
            for row in title_rs:
                isbn13 = row[0]
                isbn13_list.append(isbn13)
            title_queryset = list()
            for isbn13 in isbn13_list:
                book = Book.objects.get(isbn13=isbn13)
                title_queryset.append(book)
            title_serializer = ShortInto(title_queryset,data=request.data,many=True)
            title_serializer.is_valid(raise_exception=True)

            # 6.26日加入作者检索
            select_sql = "select isbn13 from bookdata_book where match (author_for_index)\
                          against ('+%s' in boolean mode) order by average desc limit 15;" % text_index
            cursor.execute(select_sql)
            author_rs = cursor.fetchall()

            author_isbn13_list = []
            for row in author_rs:
                isbn13 = row[0]
                author_isbn13_list.append(isbn13)
            author_queryset = list()
            for isbn13 in author_isbn13_list:
                book = Book.objects.get(isbn13=isbn13)
                author_queryset.append(book)
            # 6.28加入查询补全
            if not title_queryset and not author_queryset:
                try:
                    isbn13 = entry(key)
                    print isbn13
                    book = Book.objects.get(isbn13=isbn13)
                    title_queryset.append(book)
                except Exception as e:
                    print e
                    print e.message

            author_serializer = ShortInto(author_queryset, data=request.data, many=True)
            author_serializer.is_valid(raise_exception=True)
            reply = dict()
            reply['title_result'] = title_serializer.data
            reply['author_result'] = author_serializer.data
            print time.time()-begin
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
            # 当找不到相关书籍的时候,重新爬
            refer_list = refer_book(isbn13)
            print refer_list
            refer_object_list = list()
            if refer_list != -1:
                for i in refer_list:
                    try:
                        b = Book.objects.get(d_id=i)
                        refer_object_list.append(b)
                    except:
                        pass
                serializer = ShortInto(refer_object_list, data=request.data, many=True)
                serializer.is_valid(raise_exception=True)
                return Response(serializer.data, HTTP_200_OK)
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
    书籍分类
    """
    permission_classes =  [AllowAny]

    def get(self,request,guide_id,page):
        if page < 1:
            return Response(get_reply(81,'error page'),HTTP_404_NOT_FOUND)
        begin_page = (int(page)-1)*20
        try:
            from django.db import connection
            cursor = connection.cursor()
            sql_guide_id = str(guide_id)
            select_sql = "select isbn13 from bookdata_book where book_guide ='%s' \
            order by average desc limit %d,20;" % (sql_guide_id,begin_page+6)
            cursor.execute(select_sql)
            isbn13_rs = cursor.fetchall()
            queryset = list()
            for row in isbn13_rs:
                isbn13 = row[0]
                try:
                    book = Book.objects.get(isbn13=isbn13)
                    queryset.append(book)
                except:
                    pass
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
        # 8.30加入总页数,日期
        try:
            book = Book.objects.get(isbn13=isbn13)
            pages = book.pages
            if pages == u"('',)":
                sum_page = 300
            else:
                sum_page = int(pages)
        except:
            sum_page = 300
        import datetime
        last_date = datetime.datetime.now().date()
        read_plan = ReadPlan.objects.create(
            user=user,
            isbn13=isbn13,
            begin_time=begin_time,
            end_time=end_time,
            sum_page=sum_page,
            last_date=last_date
        )
        read_plan.save()
        return Response(get_reply(0,'success'),HTTP_201_CREATED)

    def get(self,request):
        queryset = ReadPlan.objects.filter(user=request.user)
        serializer = ReadPlanDetailSerializer(queryset,data=request.data,many=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data,HTTP_200_OK)


class ReadPlanDetailView(APIView):
    """
    删除阅读计划,得到阅读计划详情,包括打卡的记录
    """
    permission_classes = [IsAuthenticated]

    def get(self,request,pk):
        if not have_phone_register(user=request.user):
            reply = get_reply(17,'not register with phone')
            return Response(reply,HTTP_403_FORBIDDEN)
        user = request.user
        try:
            plan_item = ReadPlan.objects.get(user=user, pk=pk)
            serializer = ReadPlanDetailSerializer(plan_item, data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, HTTP_200_OK)
        except Exception as e:
            print e
            return Response(HTTP_404_NOT_FOUND)

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


class BookPriceView(APIView):
    """
    购书比价:8.25不含链接
    """
    permission_classes = [AllowAny]

    def get(self,request):
        isbn13 = request.GET.get("isbn13")
        try:
            book = Book.objects.get(isbn13=isbn13)
            title = book.title
        except:
            title = "--"
        try:
            reply = book_price(isbn13, title)
            return Response(reply,HTTP_200_OK)
        except Exception as e:
            print e
            return Response(HTTP_404_NOT_FOUND)


class ImageToTextView(APIView):
    """
    图片转换成文字
    """
    permission_classes = [AllowAny]
    serializer_class = Img2TextSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        image = serializer.validated_data['image']
        image_file = ImageFile.objects.create(image=image)
        image_file.save()
        file_name = image_file.image.url.split("/")[-1]
        try:
            result = image_to_text(file_name="./media_root/img2text/" + file_name)
            content = ''
            for words in result['words_result']:
                content += words['words']
            reply = dict()
            reply['content'] = content
            return Response(reply, HTTP_200_OK)
        except Exception as e:
            print e
            return Response(HTTP_404_NOT_FOUND)


class NoteView(APIView):
    """
    笔记,包含内容,日期,对应的书籍
    """
    permission_classes = [IsAuthenticated]
    serializer_class = NotePostSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        content = serializer.validated_data['content']
        isbn13 = serializer.validated_data['isbn13']
        comment = serializer.validated_data['comment']
        # 后端去查title和book_img_url
        try:
            book = Book.objects.get(isbn13=isbn13)
            title = book.title
            book_img_url = book.img_id
        except:
            title = u"暂无标题"
            book_img_url = u"..."
        import datetime
        date = datetime.datetime.now().date()

        note = Note.objects.create(user=user, content=content,
                                   title=title, isbn13=isbn13,
                                   date=date, comment=comment,
                                   book_img_url=book_img_url)
        note.save()
        return Response(serializer.data,HTTP_200_OK)

    def get(self, request):
        """
        查看已有的笔记
        :param request:
        :return:
        """
        user = request.user
        try:
            queryset = Note.objects.filter(user=user)
            serializer = NoteGetSerializer(queryset, data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, HTTP_200_OK)
        except Exception as e:
            print e
            return Response(HTTP_404_NOT_FOUND)


class NoteDetailView(APIView):
    """
    查看详情和删除笔记
    """

    def get(self, request, pk):
        try:
            note = Note.objects.get(user=request.user, pk=pk)
            serializer = NoteGetSerializer(note, data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, HTTP_200_OK)
        except Exception as e:
            print e
            return Response(HTTP_404_NOT_FOUND)

    def delete(self,request,pk):
        try:
            note = Note.objects.get(pk=pk)
            note.delete()
            return Response(HTTP_200_OK)
        except:
            return Response(HTTP_403_FORBIDDEN)


class NoteBookListView(APIView):
    """
    提供可以做笔记的书籍列表
    """
    def get(self,request):
        borrow_items = BorrowItem.objects.filter(user=request.user,
                                                 in_return_bar=True,
                                                 finish_return=False)
        queryset = list()
        for item in borrow_items:
            isbn13 = item.isbn13
            book = Book.objects.get(isbn13=isbn13)
            queryset.append(book)
        serializer = ShortInto(queryset, data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, HTTP_200_OK)


class PlanRecordView(APIView):
    """
    提交打卡,查看打卡详情,更新打卡
    """
    permission_classes = [IsAuthenticated]
    serializer_class = RecordPostSerializer

    def post(self, request, pk):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        now_page = serializer.validated_data['now_page']
        try:
            read_plan = ReadPlan.objects.get(pk=pk)
        except:
            return Response(HTTP_403_FORBIDDEN)
        import datetime
        record_date = datetime.datetime.now().date()
        # 这里先去查找打卡记录是否存在,存在的话直接更新
        try:
            existed_record = PlanRecord.objects.get(plan_for=read_plan,
                                                    record_date=record_date)
            existed_record.now_page = now_page
            existed_record.save()
            read_plan.now_page = now_page
            read_plan.last_date = record_date
            read_plan.save()
            return Response(HTTP_200_OK)
        except:
            last_page = read_plan.now_page
            record = PlanRecord.objects.create(plan_for=read_plan,
                                               now_page=now_page,
                                               record_date=record_date,
                                               last_page=last_page)
            record.save()
            return Response(HTTP_200_OK)

    def get(self, request,pk):
        """
        获得某个阅读计划打卡的详情
        """
        date = request.GET.get("date")
        if date:
            try:
                read_plan = ReadPlan.objects.get(pk=pk)
                record = PlanRecord.objects.get(plan_for=read_plan, record_date=date)
                serializer = RecordGetSerializer(record, data=request.data)
                serializer.is_valid(raise_exception=True)
                return Response(serializer.data, HTTP_200_OK)
            except Exception as e:
                print e
                return Response(HTTP_404_NOT_FOUND)

        else:
            try:
                read_plan = ReadPlan.objects.get(pk=pk)
                record = PlanRecord.objects.filter(plan_for=read_plan)
                serializer = RecordGetSerializer(record, data=request.data, many=True)
                serializer.is_valid(raise_exception=True)
                return Response(serializer.data,HTTP_200_OK)
            except Exception as e:
                print e
                return Response(HTTP_404_NOT_FOUND)


class PlanRecordByDateView(APIView):
    """
    显示哪些日期有打卡记录
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        date_list = list()
        record_queryset = PlanRecord.objects.filter(plan_for_id=pk)
        for record in record_queryset:
            date_list.append(record.record_date)
        return Response(date_list,HTTP_200_OK)


class AddNoteIntoCycleView(APIView):
    """
    把笔记分享到圈子
    """
    permission_classes = [IsAuthenticated]

    def get(self,request,pk):
        try:
            note = Note.objects.get(pk=pk)
            note.shared = True
            note.save()
            return Response(HTTP_200_OK)
        except Exception as e:
            print e
            return Response(HTTP_404_NOT_FOUND)



