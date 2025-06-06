from flask import Blueprint, request, jsonify
from app.models import db, Article, ArticleComment
from sqlalchemy.sql import case, func

# from flask_sqlalchemy import pagination
from app import bcrypt

article_api_bp = Blueprint("article_api", __name__)


@article_api_bp.route("/ping", methods=["GET"])
def ping():
    return jsonify({"message": "Article API Test Success"})


@article_api_bp.route("/list", methods=["GET"])
def get_article_list():
    page = request.args.get("page", default=1, type=int)
    perpage = request.args.get("perpage", default=10, type=int)
    category = request.args.get("category")

    # json에 담을 리스트 선언
    article_list = []

    # article 정보와 댓글 수 받아오기
    query = (
        Article.query.with_entities(
            Article,
            func.count(
                case((ArticleComment.status == "공개", ArticleComment.id))
            ).label("comment_count"),
        )
        .outerjoin(ArticleComment, Article.id == ArticleComment.article_id)
        .filter(Article.status == "공개")
    )

    if category:
        category = category.strip('"')
        query = query.filter(Article.category == category)

    articles = (
        query.group_by(Article.id)
        .order_by(Article.created_at.desc())
        .paginate(page=page, per_page=perpage, error_out=False)
    )

    for article, comment_count in articles:
        article_data = {
            "Id": article.id,
            "Title": article.title,
            "Category": article.category,
            "Thumbnail": article.thumbnail,
            "Description": article.description,
            "Tags": article.tags,
            "View_count": article.view_count,
            "Created_at": article.created_at,
            "Comment_count": comment_count,
        }

        article_list.append(article_data)

    return (
        jsonify(
            {
                "status": "Article 게시글 리스트 불러오기 성공",
                "articlelist": article_list,
            }
        ),
        200,
    )


@article_api_bp.route("/<string:art_id>", methods=["GET"])
def get_article(art_id):
    article = Article.query.filter_by(id=art_id).one_or_none()

    if article is None:
        return (
            jsonify({"status": "해당 id를 가진 게시글이 존재하지 않음: " + art_id}),
            404,
        )

    if article.status != "공개":
        return jsonify({"status": "게시글이 공개 상태가 아님"}), 403

    article.view_count += 1
    db.session.commit()

    article_info = {
        "Id": article.id,
        "Title": article.title,
        "Category": article.category,
        "Thumbnail": article.thumbnail,
        "Content": article.content,
        "Tags": article.tags,
        "View_count": article.view_count,
        "Created_at": article.created_at,
    }

    return (
        jsonify({"status": "게시글 상세 내용 불러오기 성공", "article": article_info}),
        200,
    )


@article_api_bp.route("/<string:art_id>/comments", methods=["GET"])
def get_comments(art_id):
    # json에 담을 리스트 선언
    comment_list = []

    # 해당 id를 가진 게시글이 있는지 확인
    check_art_id = Article.query.filter_by(id=art_id).one_or_none()

    if check_art_id is None:
        return (
            jsonify({"status": "해당 id를 가진 게시글이 존재하지 않음: " + art_id}),
            404,
        )

    # 상위 댓글 받아오기
    main_comments = (
        ArticleComment.query.filter_by(article_id=art_id, parent_id=None)
        .order_by(ArticleComment.created_at.asc())
        .all()
    )

    # 상위 댓글이 있으면 리스트에 추가하고 하위 댓글 있는지 확인해서 추가
    for maincom in main_comments:
        # sub comment 데이터를 담을 리스트 선언
        sub_list = []

        sub_comments = (
            ArticleComment.query.filter_by(parent_id=maincom.id, status="공개")
            .order_by(ArticleComment.created_at.asc())
            .all()
        )

        if len(sub_comments) > 0:
            for subcom in sub_comments:
                sub_list.append(
                    {
                        "Id": subcom.id,
                        "Content": subcom.content,
                        "Nickname": subcom.nickname,
                        "Created_at": subcom.created_at,
                        "Parent_Id": subcom.parent_id,
                    }
                )

        if maincom.status == "공개":
            comment_list.append(
                {
                    "Id": maincom.id,
                    "Content": maincom.content,
                    "Nickname": maincom.nickname,
                    "Created_at": maincom.created_at,
                    "Sub": sub_list,
                }
            )
        else:
            if len(sub_list) > 0:
                comment_list.append(
                    {
                        "Id": None,
                        "Content": "삭제된 댓글입니다.",
                        "Nickname": None,
                        "Created_at": None,
                        "Sub": sub_list,
                    }
                )

    return jsonify({"status": "댓글 받아오기 성공", "comments": comment_list}), 200


@article_api_bp.route("/<string:art_id>/comments", methods=["POST"])
def post_comments(art_id):
    data = request.json
    content = data.get("content")
    nickname = data.get("nickname")
    password = data.get("password")
    main_comment_id = data.get("comment_id")

    # 해당 id를 가진 게시글이 있는지 확인
    check_art_id = Article.query.filter_by(id=art_id).one_or_none()

    if check_art_id is None:
        return (
            jsonify({"status": "해당 id를 가진 게시글이 존재하지 않음: " + art_id}),
            404,
        )

    if main_comment_id:
        new_comment = ArticleComment(
            content=content,
            nickname=nickname,
            password=password,
            status="공개",
            article_id=art_id,
            parent_id=main_comment_id,
        )
        db.session.add(new_comment)
        db.session.commit()
    else:
        new_comment = ArticleComment(
            content=content,
            nickname=nickname,
            password=password,
            status="공개",
            article_id=art_id,
        )
        db.session.add(new_comment)
        db.session.commit()

    return jsonify({"status": "댓글 작성 성공"}), 200


@article_api_bp.route("/comments/<string:com_id>", methods=["PUT"])
def modify_comments(com_id):
    data = request.json
    content = data.get("content")
    password = data.get("password")

    comment = ArticleComment.query.filter_by(id=com_id).one_or_none()

    if comment is None:
        return (
            jsonify({"status": "해당 id를 가진 댓글이 존재하지 않음: " + com_id}),
            404,
        )

    if bcrypt.check_password_hash(comment.password, password):
        comment.content = content

        db.session.commit()

        return jsonify({"status": "댓글 수정 성공"}), 200

    return jsonify({"status": "비밀번호가 일치하지 않음", "content": content}), 401


@article_api_bp.route("/comments/<string:com_id>", methods=["DELETE"])
def delete_comments(com_id):
    data = request.json
    password = data.get("password")

    comment = ArticleComment.query.filter_by(id=com_id).one_or_none()

    if comment is None:
        return (
            jsonify({"status": "해당 id를 가진 댓글이 존재하지 않음: " + com_id}),
            404,
        )

    if bcrypt.check_password_hash(comment.password, password):
        comment.status = "비공개"

        db.session.commit()

        return jsonify({"status": "댓글 삭제 성공"}), 200

    return jsonify({"status": "비밀번호가 일치하지 않음"}), 401
