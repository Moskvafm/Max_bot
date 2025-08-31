"""
Пример магазин-бота с использованием MAX Bot Library
"""

from max_bot import Dispatcher
from max_bot.filters.base import command, text, callback_data
from max_bot.middleware.base import LoggingMiddleware


# Создаем диспетчер
dp = Dispatcher("YOUR_BOT_TOKEN")

# Каталог товаров
products = {
    "1": {"name": "Смартфон", "price": 25000, "description": "Мощный смартфон с отличной камерой"},
    "2": {"name": "Ноутбук", "price": 45000, "description": "Игровой ноутбук для работы и развлечений"},
    "3": {"name": "Наушники", "price": 5000, "description": "Беспроводные наушники с шумоподавлением"},
    "4": {"name": "Планшет", "price": 15000, "description": "Легкий планшет для чтения и работы"}
}

# Корзина пользователей
carts = {}


@dp.message_handler(command("start"))
async def start_command(message):
    """Обработчик команды /start"""
    user_id = message.from_user.id
    carts[user_id] = []
    
    welcome_text = """
🛒 Добро пожаловать в наш интернет-магазин!

Здесь вы можете:
• Просмотреть каталог товаров
• Добавить товары в корзину
• Оформить заказ

Команды:
/catalog - Каталог товаров
/cart - Ваша корзина
/order - Оформить заказ
/help - Справка

Начните с просмотра каталога!
    """
    await message.answer(welcome_text)


@dp.message_handler(command("help"))
async def help_command(message):
    """Обработчик команды /help"""
    help_text = """
🛒 Помощь по магазину

Команды:
/catalog - Просмотреть каталог товаров
/cart - Посмотреть корзину
/order - Оформить заказ
/help - Эта справка

Для добавления товара в корзину используйте команду:
/add ID_товара

Например: /add 1
    """
    await message.answer(help_text)


@dp.message_handler(command("catalog"))
async def catalog_command(message):
    """Обработчик команды /catalog"""
    catalog_text = "📦 Каталог товаров:\n\n"
    
    for product_id, product in products.items():
        catalog_text += f"ID: {product_id}\n"
        catalog_text += f"📱 {product['name']}\n"
        catalog_text += f"💰 Цена: {product['price']} ₽\n"
        catalog_text += f"📝 {product['description']}\n"
        catalog_text += f"Добавить: /add {product_id}\n\n"
    
    await message.answer(catalog_text)


@dp.message_handler(command("cart"))
async def cart_command(message):
    """Обработчик команды /cart"""
    user_id = message.from_user.id
    
    if user_id not in carts or not carts[user_id]:
        await message.answer("🛒 Ваша корзина пуста. Добавьте товары из каталога!")
        return
    
    cart_text = "🛒 Ваша корзина:\n\n"
    total = 0
    
    for product_id in carts[user_id]:
        product = products[product_id]
        cart_text += f"📱 {product['name']} - {product['price']} ₽\n"
        total += product['price']
    
    cart_text += f"\n💰 Итого: {total} ₽"
    cart_text += "\n\nДля оформления заказа используйте /order"
    
    await message.answer(cart_text)


@dp.message_handler(command("order"))
async def order_command(message):
    """Обработчик команды /order"""
    user_id = message.from_user.id
    
    if user_id not in carts or not carts[user_id]:
        await message.answer("❌ Ваша корзина пуста. Добавьте товары из каталога!")
        return
    
    total = sum(products[product_id]['price'] for product_id in carts[user_id])
    
    order_text = "📋 Оформление заказа\n\n"
    order_text += "Товары в заказе:\n"
    
    for product_id in carts[user_id]:
        product = products[product_id]
        order_text += f"• {product['name']} - {product['price']} ₽\n"
    
    order_text += f"\n💰 Итого: {total} ₽"
    order_text += "\n\n✅ Заказ оформлен! Наш менеджер свяжется с вами в ближайшее время."
    
    # Очищаем корзину
    carts[user_id] = []
    
    await message.answer(order_text)


@dp.message_handler(text=lambda text: text.startswith("/add"))
async def add_to_cart_command(message):
    """Обработчик добавления в корзину"""
    user_id = message.from_user.id
    
    try:
        product_id = message.text.split()[1]
        
        if product_id not in products:
            await message.answer("❌ Товар с таким ID не найден")
            return
        
        if user_id not in carts:
            carts[user_id] = []
        
        carts[user_id].append(product_id)
        product = products[product_id]
        
        await message.answer(f"✅ Товар '{product['name']}' добавлен в корзину!")
        
    except IndexError:
        await message.answer("❌ Используйте формат: /add ID_товара\nНапример: /add 1")


@dp.message_handler()
async def default_handler(message):
    """Обработчик по умолчанию"""
    await message.answer("Выберите команду из меню или используйте /help для справки.")


if __name__ == "__main__":
    # Добавляем middleware
    dp.add_middleware(LoggingMiddleware())
    
    # Запускаем бота
    dp.run()
