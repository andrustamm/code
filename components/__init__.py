# components/__init__.py
from .tab1_overview import render as render_tab1
from .tab2_data import render as render_tab2
from .tab3_costs import render as render_tab3
from .tab4_data_usage import render as render_tab4
from .tab5_call_duration import render as render_tab5
from .tab6_sms import render as render_tab6
from .tab7_user_stats import render as render_tab7
from .tab8_category_rules import render as render_tab8

__all__ = [
    "render_tab1",
    "render_tab2",
    "render_tab3",
    "render_tab4",
    "render_tab5",
    "render_tab6",
    "render_tab7",
    "render_tab8",
]