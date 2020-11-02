#-*- coding = utf-8 -*-
#@Time : 2020/8/13 14:42
#@Author : straightup

from django.utils.safestring import mark_safe
"""
分页组件
"""
class Pagination:
    def __init__(self, page_num, total_count, per_page_num=10, page_num_show=5):
        """
        :param page_num: 当前页码
        :param total_count: 数据总数量
        :param per_page_num: 每页展示的数据量
        :param page_num_show: 分页栏显示数量
        """
        self.total_count = total_count  #数据总条数
        self.per_page_num = per_page_num  #每页显示的条数
        self.page_num_show = page_num_show  #分页栏显示个数
        # 当前页码
        try:
            page_num = int(page_num)
        except Exception:
            page_num = 1
        self.page_num = page_num

        # 计算页码总数
        shang, yu = divmod(total_count, self.per_page_num)

        if yu:
            page_num_count = shang + 1
        else:
            page_num_count = shang

        self.page_num_count = page_num_count

        # 判断输入页码是否合理
        if page_num <= 0:
            page_num = 1
        elif page_num >= page_num_count:
            page_num = page_num_count

        half_show = self.page_num_show // 2

        if page_num - half_show <= 0:
            start_page_num = 1
            if page_num_count < per_page_num:
                end_page_num = self.page_num_count + 1
            else:
                end_page_num = self.page_num_show + 1

        elif page_num + half_show > page_num_count:
            if page_num_count <= per_page_num:
                start_page_num = 1
                end_page_num = page_num_count + 1
            else:
                start_page_num = page_num_count - page_num_show + 1
                end_page_num = page_num_count + 1

        else:
            start_page_num = page_num - half_show
            end_page_num = page_num + half_show + 1

        self.start_page_num = start_page_num
        self.end_page_num = end_page_num

    @property
    def start_data_num(self):
        return (self.page_num - 1) * self.per_page_num

    @property
    def end_data_num(self):
        return self.page_num * self.per_page_num

    # 分页模板渲染
    def pagination_html(self):
        page_num_range = range(self.start_page_num, self.end_page_num)

        page_html = ''

        # 上一页
        if self.page_num <= 1:
            per_page = '<li class="disabled"><a href="javascript:void(0)" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'
        else:
            per_page = '<li><a href="javascript:void(0)" aria-label="Previous" page="{current_page}"><span aria-hidden="true">&laquo;</span></a></li>'.format(current_page=self.page_num-1)
        page_html += per_page

        # 中间部分(重点)
        for i in page_num_range:
            if i == self.page_num:
                page_html += '<li class="active"><a href="javascript:void(0)" page="{current_page}">{current_page}</a></li>'.format(current_page=i)
            else:
                page_html += '<li><a href="javascript:void(0)" page="{current_page}">{current_page}</a></li>'.format(current_page=i)

        # 下一页
        if self.page_num >= self.page_num_count:
            page_next_html = '<li class="disabled"><a href="javascript:void(0)" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>'
        else:
            page_next_html = '<li><a href="javascript:void(0)" aria-label="Next" page="{current_page}"><span aria-hidden="true">&raquo;</span></a></li>'.format(current_page=self.page_num+1)
        page_html += page_next_html

        return mark_safe(page_html)
