from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.products.models import Category, Product
from decimal import Decimal

User = get_user_model()


class Command(BaseCommand):
    help = '初始化測試數據'

    def handle(self, *args, **options):
        # 檢查是否已初始化
        if Category.objects.exists():
            self.stdout.write(self.style.WARNING('數據已存在，跳過初始化'))
            return

        # 創建賣家帳戶
        seller, created = User.objects.get_or_create(
            username='seller_demo',
            defaults={
                'email': 'seller@easybuy.com',
                'user_type': 'seller',
                'store_name': '阿明的生活選物店',
                'is_verified': True,
            }
        )
        if created:
            seller.set_password('seller123')
            seller.save()
            self.stdout.write(self.style.SUCCESS('✓ 創建賣家帳戶: seller_demo'))
        else:
            self.stdout.write('✓ 賣家帳戶已存在')

        # 創建分類
        categories_data = [
            {'name': '生活美學', 'icon': '💡', 'description': '極簡居家裝飾'},
            {'name': '數位極客', 'icon': '💻', 'description': '高機能數位周邊'},
            {'name': '工作研務', 'icon': '📁', 'description': '工作效率工具'},
        ]

        categories = {}
        for cat_data in categories_data:
            cat, _ = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'icon': cat_data['icon'], 'description': cat_data['description']}
            )
            categories[cat_data['name']] = cat

        self.stdout.write(self.style.SUCCESS(f'✓ 創建商品分類: {len(categories)}個'))

        # 創建商品
        products_data = [
            {
                'name': '極簡原木微光檯燈',
                'category': '生活美學',
                'price': Decimal('1480.00'),
                'stock': 12,
                'description': '嚴選北美胡桃木製成，觸控三段式調光，為深夜的工作研務注入一絲溫暖光芒。',
                'status': 'onsale'
            },
            {
                'name': '航太級鋁合金人體工學架',
                'category': '數位極客',
                'price': Decimal('2280.00'),
                'stock': 8,
                'description': '多角度自由調節，完美貼合視線，防滑矽膠極致保護，極客桌面必備單品。',
                'status': 'onsale'
            },
            {
                'name': '工匠手作植鞣皮夾',
                'category': '生活美學',
                'price': Decimal('3200.00'),
                'stock': 5,
                'description': '純手工雙針手縫，選用歐洲頂級植鞣牛皮，隨時間推移展現獨一無二的溫潤色澤。',
                'status': 'onsale'
            },
            {
                'name': '高對比電子紙墨水桌鐘',
                'category': '數位極客',
                'price': Decimal('1850.00'),
                'stock': 14,
                'description': '全視角清晰可讀，內建極簡微縮番茄鐘工作法與多時區排版布局。',
                'status': 'onsale'
            },
            {
                'name': '高磅數羊毛氈隨身筆電包',
                'category': '工作研務',
                'price': Decimal('980.00'),
                'stock': 20,
                'description': '精選高密度抗震保護材質，多夾層俐落收納核心數位硬體工具。',
                'status': 'onsale'
            },
            {
                'name': '復古雙色高磅數筆記本',
                'category': '工作研務',
                'price': Decimal('420.00'),
                'stock': 25,
                'description': '180度完全平攤設計，選用頂級歐盟環保道林紙，不易透墨。',
                'status': 'onsale'
            },
            {
                'name': '多功能不鏽鋼隨行保溫杯',
                'category': '生活美學',
                'price': Decimal('890.00'),
                'stock': 0,
                'description': '真空雙層保溫技術，長效保冷保熱24小時，磨砂防滑杯身。',
                'status': 'offsale'
            },
        ]

        for prod_data in products_data:
            category = categories[prod_data['category']]
            Product.objects.get_or_create(
                name=prod_data['name'],
                seller=seller,
                defaults={
                    'category': category,
                    'price': prod_data['price'],
                    'stock': prod_data['stock'],
                    'description': prod_data['description'],
                    'status': prod_data['status'],
                }
            )

        self.stdout.write(self.style.SUCCESS(f'✓ 創建商品: {len(products_data)}個'))
        self.stdout.write(self.style.SUCCESS('✓ 數據初始化完成！'))
