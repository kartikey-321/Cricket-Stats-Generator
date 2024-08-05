from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_extension('GIGHMMPIOBKLFEPJOCNAMGKKBIGLIDOM_5_15_0_0.crx')

chrome_options.add_argument("--headless=new")


#Extract names of players to fetch the stats

df = pd.read_csv('cricket.csv')
p = df['players'].tolist()
v = df['venue'].tolist()
o = df['opponent'].tolist()

col = ['Innings']
final = []
final.append(col)

# ques = input('By venue or opponent ?')

for k in range(len(p)):
    try:
        driver = webdriver.Chrome(options=chrome_options)
        # Wait for all tabs to open
        time.sleep(5)

        # Close all tabs except the first one
        all_tabs = driver.window_handles
        for tab in all_tabs[1:]:
            driver.switch_to.window(tab)
            driver.close()

        # Switch back to the first tab
        driver.switch_to.window(all_tabs[0])
        driver.get('https://www.google.co.in')
        driver.maximize_window()
        google = driver.find_element(By.XPATH, "(//textarea[@id='APjFqb'])[1]")
        query = f"{p[k]} espncricinfo"
        google.send_keys(query)
        time.sleep(2)
        google.send_keys(Keys.RETURN)

        element = driver.find_element(By.XPATH, "(//div[@id='rso'])[1]")
        sub = element.find_element(By.TAG_NAME, 'div')
        target = sub.find_element(By.TAG_NAME, 'h3')
        target.click()

        time.sleep(5)

        bat1 = []
        bowl1 = []
        flag = 0

        try:
            driver.find_element(By.XPATH, "(//span[normalize-space()='Matches'])[1]").click()
            time.sleep(4)
            box = driver.find_element(By.TAG_NAME, 'table')
            tbody = box.find_element(By.TAG_NAME, 'tbody')
            row = tbody.find_elements(By.TAG_NAME, 'tr')
            for i in range(5):
                data = row[i].find_elements(By.TAG_NAME, 'td')
                bat1.append(data[1].text)
                bowl1.append(data[2].text)
        except:
            table = driver.find_element(By.TAG_NAME, 'table')
            tbody = table.find_element(By.TAG_NAME, 'tbody')
            row = tbody.find_elements(By.TAG_NAME, 'tr')
            for i in range(5):
                data = row[i].find_elements(By.TAG_NAME, 'td')
                bat1.append(data[1].text)
                bowl1.append(data[2].text)

        driver.close()

        bat = []
        for i in bat1:
            if '&' in i:
                bat.append(f"({i})")
            else:
                bat.append(i)

        if any(c.isalpha() for c in bowl1[0]) == True:
            flag = 1

        bowl = []
        if flag == 0:
            for i in bowl1:
                if i != '--':
                    if 'c' in i:
                        bowl.append('--')
                    elif '&' in i:
                        s = i.split('&')
                        bowl.append(f"({s[0][:1]}W & {s[1][:2]}W)")
                    else:
                        bowl.append(f"{i[:1]}W")
                else:
                    bowl.append(i)

        all = []

        for i in range(len(bat)):
            if flag == 0:
                if bat[i] == '--' and bowl[i] != '--':
                    all.append(bowl[i])
                elif bat[i] != '--' and bowl[i] == '--':
                    all.append(bat[i])
                elif bat[i] == '--' and bowl[i] == '--':
                    all.append('DNB')
                else:
                    all.append(f"{bat[i]}+{bowl[i]}")
            else:
                if bat[i] == '--':
                    all.append('DNB')
                else:
                    all.append(bat[i])

        new = []
        new.append('Recent Form')
        new.append(f"{all[0]}, {all[1]}, {all[2]}, {all[3]}, {all[4]}")
        print(new)

        ###########################cricmetric##############################
        driver = webdriver.Chrome(options=chrome_options)

        # Wait for all tabs to open
        time.sleep(5)

        # Close all tabs except the first one
        all_tabs = driver.window_handles
        for tab in all_tabs[1:]:
            driver.switch_to.window(tab)
            driver.close()

        # Switch back to the first tab
        driver.switch_to.window(all_tabs[0])

        driver.get('http://cricmetric.com')
        driver.maximize_window()

        time.sleep(5)

        driver.find_element(By.XPATH, "(//h3[@id='ui-id-1'])[1]").click()

        player = driver.find_element(By.XPATH, "//form[@action='/playerstats.py']//input[@placeholder='Add players']")

        driver.implicitly_wait(3)
        player.send_keys(p[k])

        # Wait until the suggestion is visible
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, f"//ul//li[text()='{p[k]}']"))
        )

        # time.sleep(7)
        if p[k] in ['Tom Rogers', 'Mohammad Nawaz', 'Shahadat Hossain']:
            player.send_keys(Keys.ARROW_DOWN)
            time.sleep(2)

        player.send_keys(Keys.RETURN)
    except:
        driver.close()
        continue

    driver.find_element(By.XPATH, "(//span[@role='presentation'])[1]").click()
    bat = driver.find_element(By.XPATH, "(//input[@role='searchbox'])[59]")
    bat.click()

    bat.send_keys('batting')
    # time.sleep(2)
    WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, f"//ul//li[text()='batting']"))
        )
    bat.send_keys(Keys.RETURN)

    time.sleep(2)

    driver.find_element(By.XPATH, "(//span[@role='presentation'])[2]").click()
    format = driver.find_element(By.XPATH, "(//input[@role='searchbox'])[59]")
    format.click()

    format.send_keys('Twenty20')
    # time.sleep(2)
    WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, f"//ul//li[text()='Twenty20']"))
        )
    format.send_keys(Keys.RETURN)

    time.sleep(2)

    driver.find_element(By.XPATH, "//input[@id='playerStatsCheck']").click()

    venue = driver.find_element(By.XPATH, "(//input[@placeholder='all'])[8]")
    time.sleep(2)
    venue.send_keys(v[0])
    if v[0] == 'Rajiv Gandhi International Stadium':
        venue.send_keys(Keys.ARROW_DOWN)
        time.sleep(2)
    # time.sleep(2)
    WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, f"//ul//li[text()='{v[0]}']"))
        )
    venue.send_keys(Keys.RETURN)

    driver.find_element(By.XPATH, "//form[@action='/playerstats.py']//input[@type='submit']").click()

    #############Venue Bat####################

    try:
        a = 0
        foot = driver.find_element(By.TAG_NAME, 'tfoot')
        value = foot.find_element(By.TAG_NAME, "tr")
        data = value.find_elements(By.TAG_NAME, 'td')
    except:
        print('Exception')
        a = 1

    form = []
    form.append(p[k])
    form.append(' ')
    l1_bat = []
    l1_bat.append('Venue Bat')
    if a == 0:
        line = f"Inn-{data[1].text}  R-{data[2].text}  Avg-{data[5].text}"
    else:
        line = "NA"
    l1_bat.append(line)

    #############Venue Bowl################
    time.sleep(1)

    driver.find_element(By.XPATH, "(//span[@role='presentation'])[1]").click()
    bowl = driver.find_element(By.XPATH, "(//input[@role='searchbox'])[20]")
    bowl.click()

    bowl.send_keys('bowling')
    # time.sleep(2)
    WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, f"//ul//li[text()='bowling']"))
        )
    bowl.send_keys(Keys.RETURN)

    time.sleep(2)

    driver.find_element(By.XPATH, "(//input[@type='submit'])[1]").click()

    try:
        a = 0
        foot11 = driver.find_element(By.TAG_NAME, 'tfoot')
        value11 = foot11.find_element(By.TAG_NAME, "tr")
        data11 = value11.find_elements(By.TAG_NAME, 'td')
    except:
        print('Exception')
        a = 1

    l1_bowl = []
    l1_bowl.append('Venue Bowl')
    if a == 0:
        line = f"Inn-{data11[1].text}  W-{data11[4].text}"
    else:
        line = "NA"
    l1_bowl.append(line)

    #############H2H Bat###############
    time.sleep(1)
    driver.find_element(By.XPATH, "(//span[@aria-hidden='true'][normalize-space()='×'])[2]").click()
    time.sleep(2)

    driver.find_element(By.XPATH, "(//input[@placeholder='all'])[8]").click()

    opponent = driver.find_element(By.XPATH, "(//input[@placeholder='all'])[6]")
    opponent.send_keys(o[0])
    WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, f"//ul//li[text()='{o[0]}']"))
        )
    # time.sleep(4)
    opponent.send_keys(Keys.RETURN)

    element = driver.find_element(By.XPATH, "(//span[@role='presentation'])[1]")
    driver.execute_script("arguments[0].scrollIntoView(false);", element)
    element.click()

    bat = driver.find_element(By.XPATH, "(//input[@role='searchbox'])[20]")
    bat.click()

    bat.send_keys('batting')
    # time.sleep(1)
    WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, f"//ul//li[text()='batting']"))
        )
    bat.send_keys(Keys.RETURN)

    time.sleep(2)

    driver.find_element(By.XPATH, "(//input[@type='submit'])[1]").click()

    try:
        a = 0
        foot1 = driver.find_element(By.TAG_NAME, 'tfoot')
        value1 = foot1.find_element(By.TAG_NAME, "tr")
        data1 = value1.find_elements(By.TAG_NAME, 'td')
    except:
        a = 1

    l2_bat = []
    l2_bat.append('H2H Bat')
    if a == 0:
        line = f"Inn-{data1[1].text}  R-{data1[2].text}  Avg-{data1[5].text}"
    else:
        line = "NA"
    l2_bat.append(line)

    ##################H2H Bowl################

    driver.find_element(By.XPATH, "(//span[@role='presentation'])[1]").click()
    bowl = driver.find_element(By.XPATH, "(//input[@role='searchbox'])[20]")
    bowl.click()

    bowl.send_keys('bowling')
    # time.sleep(1)
    WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, f"//ul//li[text()='bowling']"))
        )
    bowl.send_keys(Keys.RETURN)

    time.sleep(2)

    driver.find_element(By.XPATH, "(//input[@type='submit'])[1]").click()

    try:
        a = 0
        foot22 = driver.find_element(By.TAG_NAME, 'tfoot')
        value22 = foot22.find_element(By.TAG_NAME, "tr")
        data22 = value22.find_elements(By.TAG_NAME, 'td')
    except:
        a = 1

    l2_bowl = []
    l2_bowl.append('H2H Bowl')
    if a == 0:
        line = f"Inn-{data22[1].text}  W-{data22[4].text}"
    else:
        line = "NA"
    l2_bowl.append(line)

    ###################League Stats#######################

    time.sleep(1)
    driver.find_element(By.XPATH, "(//span[@aria-hidden='true'][normalize-space()='×'])[2]").click()
    time.sleep(2)

    driver.find_element(By.XPATH, "(//input[@placeholder='all'])[6]").click()

    tournament = driver.find_element(By.XPATH, "(//input[@placeholder='all'])[4]")
    tournament.send_keys("The Hundred Men's Competition")
    time.sleep(2)
    # WebDriverWait(driver, 10).until(
    #         EC.visibility_of_element_located((By.XPATH, f"//ul//li[text()='Major League Cricket']"))
    #     )
    tournament.send_keys(Keys.RETURN)

    driver.find_element(By.XPATH, "(//span[@role='presentation'])[1]").click()
    bat = driver.find_element(By.XPATH, "(//input[@role='searchbox'])[20]")
    bat.click()

    bat.send_keys('batting')
    # time.sleep(1)
    WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, f"//ul//li[text()='batting']"))
        )
    bat.send_keys(Keys.RETURN)

    time.sleep(2)

    driver.find_element(By.XPATH, "(//input[@type='submit'])[1]").click()

    try:
        a = 0
        foot2 = driver.find_element(By.TAG_NAME, 'tfoot')
        value2 = foot2.find_element(By.TAG_NAME, "tr")
        data2 = value2.find_elements(By.TAG_NAME, 'td')
    except:
        a = 1

    l4_bat = []
    l4_bat.append('The Hundred Bat')
    if a == 0:
        line = f"Inn-{data2[1].text}  R-{data2[2].text}  Avg-{data2[5].text}"
    else:
        line = "NA"
    l4_bat.append(line)

    driver.find_element(By.XPATH, "(//span[@role='presentation'])[1]").click()
    bowl = driver.find_element(By.XPATH, "(//input[@role='searchbox'])[20]")
    bowl.click()

    bowl.send_keys('bowling')
    # time.sleep(1)
    WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, f"//ul//li[text()='bowling']"))
        )
    bowl.send_keys(Keys.RETURN)

    time.sleep(2)

    driver.find_element(By.XPATH, "(//input[@type='submit'])[1]").click()

    try:
        a = 0
        foot33 = driver.find_element(By.TAG_NAME, 'tfoot')
        value33 = foot33.find_element(By.TAG_NAME, "tr")
        data33 = value33.find_elements(By.TAG_NAME, 'td')
    except:
        a = 1

    l4_bowl = []
    l4_bowl.append('The Hundred Bowl')
    if a == 0:
        line = f"Inn-{data33[1].text}  W-{data33[4].text}"
    else:
        line = "NA"
    l4_bowl.append(line)
    l3 = [' ', ' ']

    # Append collected data to the final list
    final.append(form)
    final.append(new)
    final.append(l1_bat)
    final.append(l1_bowl)
    final.append(l2_bat)
    final.append(l2_bowl)
    final.append(l4_bat)
    final.append(l4_bowl)
    final.append(l3)

    driver.close()

# Convert final list to DataFrame and save to CSV
df1 = pd.DataFrame(final)
df1.to_csv('Ultimate1.csv', index=False, header=False)
