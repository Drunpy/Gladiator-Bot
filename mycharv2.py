from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time
from colorama import init, Style, Fore, Back

init()
class gladiador:
	def __init__(self):
		self.driver = webdriver.Chrome()
		self.login()

		#Vida em %
		self.vida = 0
		#Vida real
		self.vida_real_total = 0
		self.vida_real_atual = 0

		self.exped_avl = 0
		self.masmorra_avl = 0

		for i in range(100):
			print('Ultima atualização: ', time.asctime())
			self.go()
			time.sleep(30)

	def conn(self):
		site = 'https://br.gladiatus.gameforge.com/game/'
		self.driver.get(site)

	def login(self):
		self.conn()
		seletor_login = self.driver.find_element_by_id('login_username')
		seletor_login.send_keys('') # Username

		seletor_senha = self.driver.find_element_by_id('login_password')
		seletor_senha.send_keys('') # Password

		seletor_provincia = Select(self.driver.find_element_by_id('login_server'))
		seletor_provincia.select_by_visible_text('Provincia 28')

		send_click = self.driver.find_element_by_id('loginsubmit')
		send_click.click()
	
	def back_home(self):
		time.sleep(1)
		IP_btn = self.driver.find_element_by_xpath('//*[@id="mainmenu"]/a[1]')
		IP_btn.click()
	
	def go(self):
		#Execução de tarefas
		time.sleep(2)
		self.check_role()
		try:
			self.do_masmorra()
		except:
			pass
		self.do_exped()
		self.check_role()
		self.prints()
		print('--------------------------------------------------------------')
	
	def prints(self):
		print('Vida: {}/{} ({}%)'.format(self.vida_real_atual, self.vida_real_total, self.vida))
		print('Déficit de vida: {}{}{} '.format(Back.RED, (self.vida_real_total - self.vida_real_atual), Style.RESET_ALL))

	def check_role(self):
		#Checa recursos e disponibilidades.
		exped_text = self.driver.find_element_by_id('cooldown_bar_text_expedition').text
		masmorra_text = self.driver.find_element_by_id('cooldown_bar_text_dungeon').text
		vida_text = self.driver.find_element_by_id('header_values_hp_percent').text
		vida_numeric = int(vida_text[:-1])
		#Vida em porcentagem
		self.vida = vida_numeric
		#Pega a vida total do char
		def get_total_real_life():
                        try:
                                vida_loc = self.driver.find_element_by_id('char_leben_tt')
                                vida_real_txt = vida_loc.get_attribute('data-tooltip')
                                word_m_position = vida_real_txt.find('\/')
                                #Contém o número transformado
                                vida_real_final = []
                                #contem númmeros em str da vida real
                                vida_real_strs = []
                                for i in range(3, 7):
                                        pos_of_n = vida_real_txt[word_m_position + i]
                                        try:
                                                erro_teste = pos_of_n + 1
                                        except:
                                                vida_real_strs.append(pos_of_n)				
                                join_vida_real_list = ''.join(vida_real_strs)
                                vida_real_final.append(int(join_vida_real_list))
                                return vida_real_final[0]
                        except:
                                return 0
		get_total_real_life()
		self.vida_real_total = get_total_real_life()

		def get_actual_real_life():
                        try:
                                #Pega os pontos de vida atuais
                                vida_loc = self.driver.find_element_by_id('char_leben_tt')
                                vida_real_txt = vida_loc.get_attribute('data-tooltip')
                                word_m_position = vida_real_txt.find('\/')
                                #Contém o número transformado
                                vida_real_final = []
                                #contem númmeros em str da vida real (ao contrário nesse caso)
                                vida_real_invertido = []
                                vida_real_normal = []
                                for i in range(2, 6):
                                        pos_of_n = vida_real_txt[word_m_position - i]
                                        try:
                                                int(pos_of_n) == True
                                                vida_real_invertido.append(pos_of_n)
                                        except: 
                                                pass
                                vida_real_normal = vida_real_invertido[::-1]
                                joined_v_r_n = ''.join(vida_real_normal)
                                vida_real_final.append(int(joined_v_r_n))
                                return vida_real_final[0]
                        except:
                                return 0
		get_actual_real_life()
		self.vida_real_atual = get_actual_real_life()       ##Parei aqui

		if self.vida >= 40:	
			if exped_text == 'Ir em Expedição':
				self.exped_avl = 1
			if exped_text != 'Ir em Expedição':
				self.exped_avl = 0
			if masmorra_text == 'Ir para a Masmorra':
				self.masmorra_avl = 1
			if masmorra_text != 'Ir para a Masmorra':
				self.masmorra_avl = 0
		else:
			#Caso de a vida estar baixa
			print('Saúde baixa, tentando recuperar.')
			self.back_home()
			self.recuperar_saude()

	def recuperar_saude(self):
		#Mochila 02 | CURAS
		Mochiladois_btn = self.driver.find_element_by_xpath('//*[@id="inventory_nav"]/a[2]')
		Mochiladois_btn.click()
		self.driver.execute_script("window.scrollTo(0, 350)")
		time.sleep(1)
		#Total de itens na mochila
		total_itens_bag_dois_qt = []
		given_heal_numbers = {}
		#Loop através dos itens no inventário
		try:
			for i in range(1, 40):
				heal_itens = self.driver.find_element_by_xpath('//*[@id="inv"]/div[{}]'.format(i))
				total_itens_bag_dois_qt.append(i)
				heal_item_attr_txt = heal_itens.get_attribute("data-tooltip")
				word_pos = heal_item_attr_txt.find('Cura')
				#Número final formado para ser passado pro dicio principal
				make_nums = []
				#Números único com string separados em lista
				just_nums = []
				#Loop sobre cada texto para identificação de NÚMEROS							
				for i in range(4):
					nums = heal_item_attr_txt[int(word_pos) + 5 + i]
					try:
						item_life = int(nums)
						just_nums.append(nums)
					except:
						pass	
				number = ''.join(just_nums)
				make_nums.append(number)
				num_as_int = int(make_nums[0])
				#Retorna um WebElement como key, aparentemente dá pra usar o .click() direto nele
				given_heal_numbers[heal_itens] = num_as_int
		except:
			pass
		print('Total de curas na mochila: {}'.format(len(total_itens_bag_dois_qt)))
		#print('Vida de cada item:\n{}'.format(given_heal_numbers))
		self.driver.execute_script("window.scrollTo(0, 0)")
		
	def do_exped(self):
		if self.exped_avl == 1:
			exped_btn = self.driver.find_element_by_xpath('//*[@id="cooldown_bar_expedition"]/a')
			exped_btn.click()
			#Ta separado por div, da pra analisar antes de atacar
			exped_npc_atl_btn = self.driver.find_element_by_xpath('//*[@id="expedition_list"]/div[2]/div[2]/button')
			exped_npc_atl_btn.click()
			#Fazer func pra pegar os resultados
			try:
				self.back_home()
			except:
				pass
			print('Expedição feita.')
		else:
			print('Expedição não disponível.')
	
	def do_masmorra(self):
		if self.masmorra_avl == 1:
			masmora_btn = self.driver.find_element_by_xpath('//*[@id="cooldown_bar_dungeon"]/a')
			masmora_btn.click()
			#Escolha do local | atual (Porto pirata)
			porto_pirata_btn = self.driver.find_element_by_xpath('//*[@id="submenu2"]/a[3]')
			porto_pirata_btn.click()
			#Masmorra do local
			porto_pirata_masmorra_btn = self.driver.find_element_by_xpath('//*[@id="mainnav"]/li/table/tbody/tr/td[2]/a')
			porto_pirata_masmorra_btn.click()
			#Ataca de fato
			porto_pirata_random_atk = self.driver.find_element_by_css_selector('div.map_label')
			porto_pirata_random_atk.click()
			self.back_home()
			print('Masmorra feita.')
		else:
			print('Masmorra não disponível.')
