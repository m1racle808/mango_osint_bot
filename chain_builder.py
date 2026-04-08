class ChainBuilder:
    """Управляет построением логической цепочки"""
    
    def __init__(self):
        self.steps = []  # Список шагов
        self.current_step = 0
        self.current_findings = {}
        self.last_input = None
        
    def add_step(self, input_data: str, findings: str, action: str):
        """Добавляет шаг в цепочку"""
        self.steps.append({
            'step': len(self.steps) + 1,
            'depth': self.current_step,
            'input': input_data,
            'findings': findings,
            'chosen_action': action
        })
        self.last_input = input_data
        
    def get_available_actions(self, input_type: str) -> list:
        """Возвращает доступные действия на основе типа входных данных"""
        # Демо-данные - можно расширять
        actions = {
            'email': [
                {"name": "🔍 Найти соцсети по email", "callback": "chain_social_email"},
                {"name": "💣 Проверить утечки", "callback": "chain_leaks"},
                {"name": "📧 Найти другие email'ы", "callback": "chain_other_emails"},
                {"name": "📞 Найти номер телефона", "callback": "chain_phone_from_email"}
            ],
            'phone': [
                {"name": "🔍 Найти Telegram по номеру", "callback": "chain_tg_from_phone"},
                {"name": "🏦 Пробить оператора", "callback": "chain_operator"},
                {"name": "📧 Найти email по номеру", "callback": "chain_email_from_phone"}
            ],
            'username': [
                {"name": "🌐 Поиск по соцсетям", "callback": "chain_social_username"},
                {"name": "📊 Анализ активности", "callback": "chain_activity"},
                {"name": "🖼️ Найти фото", "callback": "chain_photos"}
            ]
        }
        
        for key, action_list in actions.items():
            if key in input_type.lower() or self._guess_input_type(input_type) == key:
                return action_list
        
        # Дефолтные действия
        return [
            {"name": "🔍 Продолжить поиск", "callback": "chain_continue"},
            {"name": "✅ Завершить", "callback": "finish_chain"}
        ]
    
    def _guess_input_type(self, text: str) -> str:
        """Угадывает тип входных данных"""
        if '@' in text:
            return 'email'
        elif any(c.isdigit() for c in text) and len(text) > 5:
            return 'phone'
        else:
            return 'username'
    
    def process_action(self, action: str, input_data: str = None) -> dict:
        """Обрабатывает выбранное действие и возвращает результат"""
        # Демо-данные - здесь можно подключать реальные API
        demo_results = {
            'chain_social_email': "Telegram: @user_tg, VK: vk.com/user, Twitter: @user_tw",
            'chain_leaks': "Найден пароль в утечке 2023: password123, email засвечен на 5 сайтах",
            'chain_other_emails': "user.work@gmail.com, user_old@mail.ru",
            'chain_phone_from_email': "+7 999 123-45-67",
            'chain_tg_from_phone': "Telegram: @user_by_phone",
            'chain_operator': "Оператор: МТС, регион: Москва",
            'chain_email_from_phone': "phoneuser@mail.ru",
            'chain_social_username': "Instagram: @user, TikTok: @user",
            'chain_activity': "Активен вечером, посты на тему IT",
            'chain_photos': "Найдено 3 фотографии по username"
        }
        
        result = demo_results.get(action, "Дополнительная информация найдена")
        
        self.current_step += 1
        self.add_step(
            input_data or self.last_input,
            result,
            action
        )
        
        return {
            'findings': result,
            'next_actions': self.get_available_actions(result)
        }
    
    def get_final_findings(self) -> dict:
        """Собирает итоговые выводы"""
        all_findings = {}
        for step in self.steps:
            all_findings[f"Шаг {step['step']}"] = step['findings'][:100]
        return all_findings
    
    def get_chain_data(self) -> list:
        """Возвращает все шаги цепочки"""
        return self.steps
    
    def reset(self):
        """Сбрасывает цепочку"""
        self.steps = []
        self.current_step = 0
        self.current_findings = {}
        self.last_input = None
