import customtkinter as ctk

class Theme:
    # 색상 팔레트
    COLORS = {
        # 메인 컬러 (치과 전문적인 느낌)
        'primary': '#2C5F7C',      # 진한 청록색
        'primary_hover': '#1E4A63', # 더 진한 청록색
        'secondary': '#4A9EBF',    # 밝은 청록색
        'accent': '#7FB8CC',       # 연한 청록색
        
        # 기능별 컬러
        'success': '#4CAF50',      # 녹색
        'warning': '#FF9800',      # 주황색
        'error': '#F44336',        # 빨간색
        'info': '#2196F3',         # 파란색
        
        # 중성 컬러
        'light_gray': '#F5F5F5',
        'medium_gray': '#E0E0E0',
        'dark_gray': '#757575',
        'text_primary': '#212121',
        'text_secondary': '#757575',
        
        # 배경
        'bg_primary': '#FFFFFF',
        'bg_secondary': '#FAFAFA',
        'bg_card': '#FFFFFF',
        
        # 연차 타입별 컬러
        'leave_annual': '#4CAF50',      # 연차 - 녹색
        'leave_half': '#FF9800',        # 반차 - 주황색
        'leave_sick': '#F44336',        # 병가 - 빨간색
        'leave_event': '#9C27B0',       # 경조사 - 보라색
        'leave_common': '#2196F3',      # 공통연차 - 파란색
    }
    
    # 폰트 설정 (함수로 변경하여 lazy loading)
    @staticmethod
    def get_font(font_type):
        """필요할 때 폰트 생성"""
        fonts = {
            'title': lambda: ctk.CTkFont(family="맑은 고딕", size=24, weight="bold"),
            'subtitle': lambda: ctk.CTkFont(family="맑은 고딕", size=18, weight="bold"),
            'header': lambda: ctk.CTkFont(family="맑은 고딕", size=16, weight="bold"),
            'body': lambda: ctk.CTkFont(family="맑은 고딕", size=12),
            'body_bold': lambda: ctk.CTkFont(family="맑은 고딕", size=12, weight="bold"),
            'caption': lambda: ctk.CTkFont(family="맑은 고딕", size=10),
            'button': lambda: ctk.CTkFont(family="맑은 고딕", size=12, weight="bold"),
        }
        return fonts.get(font_type, lambda: ctk.CTkFont(size=12))()
    
    # 버튼 스타일 (함수로 변경)
    @staticmethod
    def get_button_style(style_name):
        """버튼 스타일 가져오기"""
        styles = {
            'primary': {
                'fg_color': Theme.COLORS['primary'],
                'hover_color': Theme.COLORS['primary_hover'],
                'font': Theme.get_font('button'),
                'corner_radius': 8,
                'height': 36
            },
            'secondary': {
                'fg_color': Theme.COLORS['secondary'],
                'hover_color': Theme.COLORS['primary'],
                'font': Theme.get_font('button'),
                'corner_radius': 8,
                'height': 36
            },
            'success': {
                'fg_color': Theme.COLORS['success'],
                'hover_color': '#45A049',
                'font': Theme.get_font('button'),
                'corner_radius': 8,
                'height': 36
            },
            'warning': {
                'fg_color': Theme.COLORS['warning'],
                'hover_color': '#E68900',
                'font': Theme.get_font('button'),
                'corner_radius': 8,
                'height': 36
            },
            'error': {
                'fg_color': Theme.COLORS['error'],
                'hover_color': '#D32F2F',
                'font': Theme.get_font('button'),
                'corner_radius': 8,
                'height': 36
            }
        }
        return styles.get(style_name, styles['primary'])
    
    # 프레임 스타일
    FRAME_STYLES = {
        'card': {
            'corner_radius': 12,
            'border_width': 1,
            'border_color': COLORS['medium_gray'],
            'fg_color': COLORS['bg_card']
        },
        'sidebar': {
            'corner_radius': 0,
            'fg_color': COLORS['primary'],
            'border_width': 0
        },
        'content': {
            'corner_radius': 8,
            'fg_color': COLORS['bg_secondary'],
            'border_width': 0
        }
    }
    
    @staticmethod
    def apply_button_style(button, style_name='primary'):
        """버튼에 테마 스타일 적용"""
        style = Theme.get_button_style(style_name)
        button.configure(**style)
    
    @staticmethod
    def apply_frame_style(frame, style_name='card'):
        """프레임에 테마 스타일 적용"""
        if style_name in Theme.FRAME_STYLES:
            style = Theme.FRAME_STYLES[style_name]
            frame.configure(**style)
    
    @staticmethod
    def get_leave_color(leave_type):
        """연차 타입에 따른 색상 반환"""
        if leave_type == '연차':
            return Theme.COLORS['leave_annual']
        elif '반차' in leave_type:
            return Theme.COLORS['leave_half']
        elif leave_type == '병가':
            return Theme.COLORS['leave_sick']
        elif leave_type == '경조사':
            return Theme.COLORS['leave_event']
        else:
            return Theme.COLORS['leave_common']