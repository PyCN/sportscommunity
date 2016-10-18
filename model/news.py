#!/usr/bin/env python
# coding=utf-8
import _env  # noqa
from mongo import Doc
from controller.tools import DateTime


class News(Doc):

    structure = dict(
        title=str,
        author=str,
        source=str,
        image=str,
        tag=str,
        keyword=str,
        content=str,
        flow=str,
        datetime=str,
        comment=dict,
        createdTime=str,
        deleted=bool
    )

    _t = DateTime()

    default_values = {
        'createdTime': _t.current_time,
        'deleted': False
    }

    @classmethod
    def _create(cls, **kwargs):
        news = News(dict(
            title=kwargs.get('title', ''),
            author=kwargs.get('author', ''),
            source=kwargs.get('source', ''),
            image=kwargs.get('image', ''),
            tag=kwargs.get('tag', ''),
            keyword=kwargs.get('keyword', ''),
            content=kwargs.get('content', ''),
            flow=kwargs.get('flow', ''),
            datetime=kwargs.get('datetime', ''),
            comment=kwargs.get('comment') if kwargs.get('comment') else {}
        ), True)
        news.save()
