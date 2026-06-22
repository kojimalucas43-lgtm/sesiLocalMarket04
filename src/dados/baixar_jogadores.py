import os
import time
import json
from io import BytesIO
import requests
from PIL import Image, ImageOps
from ddgs import DDGS

# O seu JSON mapeado
dados_json = """
[
  { "id": 1, "desc": "Larry Bird", "team": "Boston Celtics", "imagem": "../../public/bird.jpg", "sal": 7070000.00 },
  { "id": 2, "desc": "Bill Russell", "team": "Boston Celtics", "imagem": "../../public/russell.jpg", "sal": 100000.00 },
  { "id": 3, "desc": "Paul Pierce", "team": "Boston Celtics", "imagem": "../../public/pierce.jpg", "sal": 19806800.00 },
  { "id": 4, "desc": "Bob Cousy", "team": "Boston Celtics", "imagem": "../../public/cousy.jpg", "sal": 35000.00 },
  { "id": 5, "desc": "John Havlicek", "team": "Boston Celtics", "imagem": "../../public/havlicek.jpg", "sal": 300000.00 },
  { "id": 6, "desc": "Jason Kidd", "team": "Brooklyn Nets", "imagem": "../../public/kidd.jpg", "sal": 18084000.00 },
  { "id": 7, "desc": "Vince Carter", "team": "Brooklyn Nets", "imagem": "../../public/carter_nets.jpg", "sal": 13550000.00 },
  { "id": 8, "desc": "Kevin Durant", "team": "Brooklyn Nets", "imagem": "../../public/durant_nets.jpg", "sal": 42018900.00 },
  { "id": 9, "desc": "Brook Lopez", "team": "Brooklyn Nets", "imagem": "../../public/lopez.jpg", "sal": 22642350.00 },
  { "id": 10, "desc": "Richard Jefferson", "team": "Brooklyn Nets", "imagem": "../../public/jefferson.jpg", "sal": 13000000.00 },
  { "id": 11, "desc": "Walt Frazier", "team": "New York Knicks", "imagem": "../../public/frazier.jpg", "sal": 450000.00 },
  { "id": 12, "desc": "Patrick Ewing", "team": "New York Knicks", "imagem": "../../public/ewing.jpg", "sal": 18724000.00 },
  { "id": 13, "desc": "Willis Reed", "team": "New York Knicks", "imagem": "../../public/reed.jpg", "sal": 200000.00 },
  { "id": 14, "desc": "Bernard King", "team": "New York Knicks", "imagem": "../../public/king.jpg", "sal": 2200000.00 },
  { "id": 15, "desc": "Allan Houston", "team": "New York Knicks", "imagem": "../../public/houston.jpg", "sal": 15125000.00 },
  { "id": 16, "desc": "Allen Iverson", "team": "Philadelphia 76ers", "imagem": "../../public/iverson.jpg", "sal": 10130000.00 },
  { "id": 17, "desc": "Julius Erving", "team": "Philadelphia 76ers", "imagem": "../../public/erving.jpg", "sal": 2000000.00 },
  { "id": 18, "desc": "Wilt Chamberlain", "team": "Philadelphia 76ers", "imagem": "../../public/chamberlain_phi.jpg", "sal": 250000.00 },
  { "id": 19, "desc": "Charles Barkley", "team": "Philadelphia 76ers", "imagem": "../../public/barkley_phi.jpg", "sal": 3900000.00 },
  { "id": 20, "desc": "Hal Greer", "team": "Philadelphia 76ers", "imagem": "../../public/greer.jpg", "sal": 100000.00 },
  { "id": 21, "desc": "Vince Carter", "team": "Toronto Raptors", "imagem": "../../public/carter_tor.jpg", "sal": 12340000.00 },
  { "id": 22, "desc": "Chris Bosh", "team": "Toronto Raptors", "imagem": "../../public/bosh_tor.jpg", "sal": 14410581.00 },
  { "id": 23, "desc": "Kyle Lowry", "team": "Toronto Raptors", "imagem": "../../public/lowry.jpg", "sal": 31999999.00 },
  { "id": 24, "desc": "DeMar DeRozan", "team": "Toronto Raptors", "imagem": "../../public/derozan.jpg", "sal": 26012500.00 },
  { "id": 25, "desc": "Kawhi Leonard", "team": "Toronto Raptors", "imagem": "../../public/leonard_tor.jpg", "sal": 32742000.00 },
  { "id": 26, "desc": "Michael Jordan", "team": "Chicago Bulls", "imagem": "../../public/jordan.jpg", "sal": 33140000.00 },
  { "id": 27, "desc": "Scottie Pippen", "team": "Chicago Bulls", "imagem": "../../public/pippen.jpg", "sal": 2775000.00 },
  { "id": 28, "desc": "Dennis Rodman", "team": "Chicago Bulls", "imagem": "../../public/rodman.jpg", "sal": 9000000.00 },
  { "id": 29, "desc": "Derrick Rose", "team": "Chicago Bulls", "imagem": "../../public/rose.jpg", "sal": 16402500.00 },
  { "id": 30, "desc": "Bob Love", "team": "Chicago Bulls", "imagem": "../../public/love_chi.jpg", "sal": 340000.00 },
  { "id": 31, "desc": "LeBron James", "team": "Cleveland Cavaliers", "imagem": "../../public/lebron_cle.jpg", "sal": 22970500.00 },
  { "id": 32, "desc": "Kyrie Irving", "team": "Cleveland Cavaliers", "imagem": "../../public/irving_cle.jpg", "sal": 17118750.00 },
  { "id": 33, "desc": "Kevin Love", "team": "Cleveland Cavaliers", "imagem": "../../public/love_cle.jpg", "sal": 21165675.00 },
  { "id": 34, "desc": "Mark Price", "team": "Cleveland Cavaliers", "imagem": "../../public/price.jpg", "sal": 3500000.00 },
  { "id": 35, "desc": "Brad Daugherty", "team": "Cleveland Cavaliers", "imagem": "../../public/daugherty.jpg", "sal": 5200000.00 },
  { "id": 36, "desc": "Isiah Thomas", "team": "Detroit Pistons", "imagem": "../../public/thomas_det.jpg", "sal": 3000000.00 },
  { "id": 37, "desc": "Joe Dumars", "team": "Detroit Pistons", "imagem": "../../public/dumars.jpg", "sal": 4000000.00 },
  { "id": 38, "desc": "Bill Laimbeer", "team": "Detroit Pistons", "imagem": "../../public/laimbeer.jpg", "sal": 3000000.00 },
  { "id": 39, "desc": "Grant Hill", "team": "Detroit Pistons", "imagem": "../../public/hill_det.jpg", "sal": 9000000.00 },
  { "id": 40, "desc": "Chauncey Billups", "team": "Detroit Pistons", "imagem": "../../public/billups.jpg", "sal": 11000000.00 },
  { "id": 41, "desc": "Reggie Miller", "team": "Indiana Pacers", "imagem": "../../public/miller.jpg", "sal": 9000000.00 },
  { "id": 42, "desc": "Rik Smits", "team": "Indiana Pacers", "imagem": "../../public/smits.jpg", "sal": 5100000.00 },
  { "id": 43, "desc": "Paul George", "team": "Indiana Pacers", "imagem": "../../public/george_ind.jpg", "sal": 17116667.00 },
  { "id": 44, "desc": "Jermaine O'Neal", "team": "Indiana Pacers", "imagem": "../../public/oneal_ind.jpg", "sal": 15750000.00 },
  { "id": 45, "desc": "Mark Jackson", "team": "Indiana Pacers", "imagem": "../../public/jackson_ind.jpg", "sal": 4500000.00 },
  { "id": 46, "desc": "Kareem Abdul-Jabbar", "team": "Milwaukee Bucks", "imagem": "../../public/kareem_mil.jpg", "sal": 350000.00 },
  { "id": 47, "desc": "Oscar Robertson", "team": "Milwaukee Bucks", "imagem": "../../public/robertson.jpg", "sal": 250000.00 },
  { "id": 48, "desc": "Giannis Antetokounmpo", "team": "Milwaukee Bucks", "imagem": "../../public/giannis.jpg", "sal": 39344900.00 },
  { "id": 49, "desc": "Bob Dandridge", "team": "Milwaukee Bucks", "imagem": "../../public/dandridge.jpg", "sal": 200000.00 },
  { "id": 50, "desc": "Jon McGlocklin", "team": "Milwaukee Bucks", "imagem": "../../public/mcglocklin.jpg", "sal": 100000.00 },
  { "id": 51, "desc": "Dominique Wilkins", "team": "Atlanta Hawks", "imagem": "../../public/wilkins.jpg", "sal": 4000000.00 },
  { "id": 52, "desc": "Lou Hudson", "team": "Atlanta Hawks", "imagem": "../../public/hudson.jpg", "sal": 200000.00 },
  { "id": 53, "desc": "Pete Maravich", "team": "Atlanta Hawks", "imagem": "../../public/maravich.jpg", "sal": 600000.00 },
  { "id": 54, "desc": "Bob Pettit", "team": "Atlanta Hawks", "imagem": "../../public/pettit.jpg", "sal": 50000.00 },
  { "id": 55, "desc": "Kevin Willis", "team": "Atlanta Hawks", "imagem": "../../public/willis.jpg", "sal": 2000000.00 },
  { "id": 56, "desc": "Alonzo Mourning", "team": "Charlotte Hornets", "imagem": "../../public/mourning_cha.jpg", "sal": 4800000.00 },
  { "id": 57, "desc": "Larry Johnson", "team": "Charlotte Hornets", "imagem": "../../public/johnson_cha.jpg", "sal": 11500000.00 },
  { "id": 58, "desc": "Muggsy Bogues", "team": "Charlotte Hornets", "imagem": "../../public/bogues.jpg", "sal": 2500000.00 },
  { "id": 59, "desc": "Glen Rice", "team": "Charlotte Hornets", "imagem": "../../public/rice_cha.jpg", "sal": 2700000.00 },
  { "id": 60, "desc": "Dell Curry", "team": "Charlotte Hornets", "imagem": "../../public/curry_dell.jpg", "sal": 2500000.00 },
  { "id": 61, "desc": "LeBron James", "team": "Miami Heat", "imagem": "../../public/lebron_mia.jpg", "sal": 17545000.00 },
  { "id": 62, "desc": "Dwyane Wade", "team": "Miami Heat", "imagem": "../../public/wade.jpg", "sal": 14200000.00 },
  { "id": 63, "once_id": 63, "desc": "Alonzo Mourning", "team": "Miami Heat", "imagem": "../../public/mourning_mia.jpg", "sal": 15004000.00 },
  { "id": 64, "desc": "Chris Bosh", "team": "Miami Heat", "imagem": "../../public/bosh_mia.jpg", "sal": 17545000.00 },
  { "id": 65, "desc": "Tim Hardaway", "team": "Miami Heat", "imagem": "../../public/hardaway_mia.jpg", "sal": 9000000.00 },
  { "id": 66, "desc": "Shaquille O'Neal", "team": "Orlando Magic", "imagem": "../../public/shaq_orl.jpg", "sal": 5000000.00 },
  { "id": 67, "desc": "Penny Hardaway", "team": "Orlando Magic", "imagem": "../../public/hardaway_pen.jpg", "sal": 4990000.00 },
  { "id": 68, "desc": "Dwight Howard", "team": "Orlando Magic", "imagem": "../../public/howard_orl.jpg", "sal": 17176440.00 },
  { "id": 69, "desc": "Nick Anderson", "team": "Orlando Magic", "imagem": "../../public/anderson_orl.jpg", "sal": 4100000.00 },
  { "id": 70, "desc": "Dennis Scott", "team": "Orlando Magic", "imagem": "../../public/scott_orl.jpg", "sal": 3000000.00 },
  { "id": 71, "desc": "Elvin Hayes", "team": "Washington Wizards", "imagem": "../../public/hayes.jpg", "sal": 500000.00 },
  { "id": 72, "desc": "Wes Unseld", "team": "Washington Wizards", "imagem": "../../public/unseld.jpg", "sal": 400000.00 },
  { "id": 73, "desc": "Gilbert Arenas", "team": "Washington Wizards", "imagem": "../../public/arenas.jpg", "sal": 16318452.00 },
  { "id": 74, "desc": "John Wall", "team": "Washington Wizards", "imagem": "../../public/wall.jpg", "sal": 19263750.00 },
  { "id": 75, "desc": "Bradley Beal", "team": "Washington Wizards", "imagem": "../../public/beal.jpg", "sal": 28751775.00 },
  { "id": 76, "desc": "Alex English", "team": "Denver Nuggets", "imagem": "../../public/english.jpg", "sal": 2000000.00 },
  { "id": 77, "desc": "David Thompson", "team": "Denver Nuggets", "imagem": "../../public/thompson_den.jpg", "sal": 800000.00 },
  { "id": 78, "desc": "Dan Issel", "team": "Denver Nuggets", "imagem": "../../public/issel.jpg", "sal": 500000.00 },
  { "id": 79, "desc": "Carmelo Anthony", "team": "Denver Nuggets", "imagem": "../../public/anthony_den.jpg", "sal": 16544310.00 },
  { "id": 80, "desc": "Nikola Jokic", "team": "Denver Nuggets", "imagem": "../../public/jokic.jpg", "sal": 29542010.00 },
  { "id": 81, "desc": "Kevin Garnett", "team": "Minnesota Timberwolves", "imagem": "../../public/garnett_min.jpg", "sal": 28000000.00 },
  { "id": 82, "desc": "Stephon Marbury", "team": "Minnesota Timberwolves", "imagem": "../../public/marbury.jpg", "sal": 4800000.00 },
  { "id": 83, "desc": "Tom Gugliotta", "team": "Minnesota Timberwolves", "imagem": "../../public/gugliotta.jpg", "sal": 7800000.00 },
  { "id": 84, "desc": "Wally Szczerbiak", "team": "Minnesota Timberwolves", "imagem": "../../public/szczerbiak.jpg", "sal": 8000000.00 },
  { "id": 85, "desc": "Karl-Anthony Towns", "team": "Minnesota Timberwolves", "imagem": "../../public/towns.jpg", "sal": 29342920.00 },
  { "id": 86, "desc": "Kevin Durant", "team": "Oklahoma City Thunder", "imagem": "../../public/durant_okc.jpg", "sal": 19450000.00 },
  { "id": 87, "desc": "Russell Westbrook", "team": "Oklahoma City Thunder", "imagem": "../../public/westbrook.jpg", "sal": 17884654.00 },
  { "id": 88, "desc": "James Harden", "team": "Oklahoma City Thunder", "imagem": "../../public/harden_okc.jpg", "sal": 3847000.00 },
  { "id": 89, "desc": "Serge Ibaka", "team": "Oklahoma City Thunder", "imagem": "../../public/ibaka.jpg", "sal": 12250000.00 },
  { "id": 90, "desc": "Nick Collison", "team": "Oklahoma City Thunder", "imagem": "../../public/collison.jpg", "sal": 3500000.00 },
  { "id": 91, "desc": "Clyde Drexler", "team": "Portland Trail Blazers", "imagem": "../../public/drexler.jpg", "sal": 4500000.00 },
  { "id": 92, "desc": "Bill Walton", "team": "Portland Trail Blazers", "imagem": "../../public/walton.jpg", "sal": 350000.00 },
  { "id": 93, "desc": "Terry Porter", "team": "Portland Trail Blazers", "imagem": "../../public/porter.jpg", "sal": 3500000.00 },
  { "id": 94, "desc": "Damian Lillard", "team": "Portland Trail Blazers", "imagem": "../../public/lillard.jpg", "sal": 30750000.00 },
  { "id": 95, "desc": "Brandon Roy", "team": "Portland Trail Blazers", "imagem": "../../public/roy.jpg", "sal": 12700000.00 },
  { "id": 96, "desc": "Karl Malone", "team": "Utah Jazz", "imagem": "../../public/malone_utah.jpg", "sal": 7500000.00 },
  { "id": 97, "desc": "John Stockton", "team": "Utah Jazz", "imagem": "../../public/stockton.jpg", "sal": 4800000.00 },
  { "id": 98, "desc": "Adrian Dantley", "team": "Utah Jazz", "imagem": "../../public/dantley.jpg", "sal": 1000000.00 },
  { "id": 99, "desc": "Jeff Hornacek", "team": "Utah Jazz", "imagem": "../../public/hornacek.jpg", "sal": 4600000.00 },
  { "id": 100, "desc": "Mark Eaton", "team": "Utah Jazz", "imagem": "../../public/eaton.jpg", "sal": 2000000.00 },
  { "id": 101, "desc": "Stephen Curry", "team": "Golden State Warriors", "imagem": "../../public/curry.jpg", "sal": 34682550.00 },
  { "id": 102, "desc": "Klay Thompson", "team": "Golden State Warriors", "imagem": "../../public/thompson_gs.jpg", "sal": 18988725.00 },
  { "id": 103, "desc": "Draymond Green", "team": "Golden State Warriors", "imagem": "../../public/green_gs.jpg", "sal": 17469565.00 },
  { "id": 104, "desc": "Kevin Durant", "team": "Golden State Warriors", "imagem": "../../public/durant_gs.jpg", "sal": 30000000.00 },
  { "id": 105, "desc": "Wilt Chamberlain", "team": "Golden State Warriors", "imagem": "../../public/chamberlain_gs.jpg", "sal": 65000.00 },
  { "id": 106, "desc": "Chris Paul", "team": "Los Angeles Clippers", "imagem": "../../public/paul_lac.jpg", "sal": 21468695.00 },
  { "id": 107, "desc": "Blake Griffin", "team": "Los Angeles Clippers", "imagem": "../../public/griffin.jpg", "sal": 20140838.00 },
  { "id": 108, "desc": "DeAndre Jordan", "team": "Los Angeles Clippers", "imagem": "../../public/jordan_lac.jpg", "sal": 21165675.00 },
  { "id": 109, "desc": "Bob McAdoo", "team": "Los Angeles Clippers", "imagem": "../../public/mcadoo.jpg", "sal": 600000.00 },
  { "id": 110, "desc": "Randy Smith", "team": "Los Angeles Clippers", "imagem": "../../public/smith_lac.jpg", "sal": 250000.00 },
  { "id": 111, "desc": "Magic Johnson", "team": "Los Angeles Lakers", "imagem": "../../public/magic.jpg", "sal": 2500000.00 },
  { "id": 112, "desc": "Kobe Bryant", "team": "Los Angeles Lakers", "imagem": "../../public/kobe.jpg", "sal": 30464200.00 },
  { "id": 113, "desc": "Shaquille O'Neal", "team": "Los Angeles Lakers", "imagem": "../../public/shaq_lal.jpg", "sal": 29000000.00 },
  { "id": 114, "desc": "Kareem Abdul-Jabbar", "team": "Los Angeles Lakers", "imagem": "../../public/kareem_lal.jpg", "sal": 3000000.00 },
  { "id": 115, "desc": "Jerry West", "team": "Los Angeles Lakers", "imagem": "../../public/west.jpg", "sal": 200000.00 },
  { "id": 116, "desc": "Steve Nash", "team": "Phoenix Suns", "imagem": "../../public/nash.jpg", "sal": 13500000.00 },
  { "id": 117, "desc": "Charles Barkley", "team": "Phoenix Suns", "imagem": "../../public/barkley_phx.jpg", "sal": 5000000.00 },
  { "id": 118, "desc": "Kevin Johnson", "team": "Phoenix Suns", "imagem": "../../public/johnson_phx.jpg", "sal": 5000000.00 },
  { "id": 119, "desc": "Amar'e Stoudemire", "team": "Phoenix Suns", "imagem": "../../public/stoudemire.jpg", "sal": 14410581.00 },
  { "id": 120, "desc": "Devin Booker", "team": "Phoenix Suns", "imagem": "../../public/booker.jpg", "sal": 31650600.00 },
  { "id": 121, "desc": "Oscar Robertson", "team": "Sacramento Kings", "imagem": "../../public/robertson_sac.jpg", "sal": 100000.00 },
  { "id": 122, "desc": "Chris Webber", "team": "Sacramento Kings", "imagem": "../../public/webber.jpg", "sal": 17777000.00 },
  { "id": 123, "desc": "Mitch Richmond", "team": "Sacramento Kings", "imagem": "../../public/richmond.jpg", "sal": 5500000.00 },
  { "id": 124, "desc": "Vlade Divac", "team": "Sacramento Kings", "imagem": "../../public/divac.jpg", "sal": 4500000.00 },
  { "id": 125, "desc": "Mike Bibby", "team": "Sacramento Kings", "imagem": "../../public/bibby.jpg", "sal": 9200000.00 },
  { "id": 126, "desc": "Dirk Nowitzki", "team": "Dallas Mavericks", "imagem": "../../public/nowitzki.jpg", "sal": 25000000.00 },
  { "id": 127, "desc": "Jason Kidd", "team": "Dallas Mavericks", "imagem": "../../public/kidd_dal.jpg", "sal": 11700000.00 },
  { "id": 128, "desc": "Luka Doncic", "team": "Dallas Mavericks", "imagem": "../../public/doncic.jpg", "sal": 37096500.00 },
  { "id": 129, "desc": "Mark Aguirre", "team": "Dallas Mavericks", "imagem": "../../public/aguirre.jpg", "sal": 1500000.00 },
  { "id": 130, "desc": "Rolando Blackman", "team": "Dallas Mavericks", "imagem": "../../public/blackman.jpg", "sal": 1000000.00 },
  { "id": 131, "desc": "Hakeem Olajuwon", "team": "Houston Rockets", "imagem": "../../public/olajuwon.jpg", "sal": 8000000.00 },
  { "id": 132, "desc": "Clyde Drexler", "team": "Houston Rockets", "imagem": "../../public/drexler_hou.jpg", "sal": 9500000.00 },
  { "id": 133, "desc": "James Harden", "team": "Houston Rockets", "imagem": "../../public/harden_hou.jpg", "sal": 35654150.00 },
  { "id": 134, "desc": "Calvin Murphy", "team": "Houston Rockets", "imagem": "../../public/murphy.jpg", "sal": 400000.00 },
  { "id": 135, "desc": "Yao Ming", "team": "Houston Rockets", "imagem": "../../public/yao.jpg", "sal": 17690000.00 },
  { "id": 136, "desc": "Pau Gasol", "team": "Memphis Grizzlies", "imagem": "../../public/gasol_mem.jpg", "sal": 5900000.00 },
  { "id": 137, "desc": "Tony Allen", "team": "Memphis Grizzlies", "imagem": "../../public/allen_mem.jpg", "sal": 5300000.00 },
  { "id": 138, "desc": "Marc Gasol", "team": "Memphis Grizzlies", "imagem": "../../public/gasol_marc.jpg", "sal": 21153659.00 },
  { "id": 139, "desc": "Mike Conley", "team": "Memphis Grizzlies", "imagem": "../../public/conley.jpg", "sal": 28530608.00 },
  { "id": 140, "desc": "Zach Randolph", "team": "Memphis Grizzlies", "imagem": "../../public/randolph.jpg", "sal": 16500000.00 },
  { "id": 141, "desc": "Chris Paul", "team": "New Orleans Pelicans", "imagem": "../../public/paul_no.jpg", "sal": 16354800.00 },
  { "id": 142, "desc": "Anthony Davis", "team": "New Orleans Pelicans", "imagem": "../../public/davis.jpg", "sal": 27093000.00 },
  { "id": 143, "desc": "David West", "team": "New Orleans Pelicans", "imagem": "../../public/west_no.jpg", "sal": 8300000.00 },
  { "id": 144, "desc": "Peja Stojakovic", "team": "New Orleans Pelicans", "imagem": "../../public/stojakovic.jpg", "sal": 14000000.00 },
  { "id": 145, "desc": "Zion Williamson", "team": "New Orleans Pelicans", "imagem": "../../public/zion.jpg", "sal": 35710600.00 },
  { "id": 146, "desc": "Tim Duncan", "team": "San Antonio Spurs", "imagem": "../../public/duncan.jpg", "sal": 14800000.00 },
  { "id": 147, "desc": "Tony Parker", "team": "San Antonio Spurs", "imagem": "../../public/parker.jpg", "sal": 12500000.00 },
  { "id": 148, "desc": "Manu Ginobili", "team": "San Antonio Spurs", "imagem": "../../public/ginobili.jpg", "sal": 14300000.00 },
  { "id": 149, "desc": "David Robinson", "team": "San Antonio Spurs", "imagem": "../../public/robinson.jpg", "sal": 6250000.00 },
  { "id": 150, "desc": "George Gervin", "team": "San Antonio Spurs", "imagem": "../../public/gervin.jpg", "sal": 500000.00 }
]
"""

# Carrega a string JSON como lista do Python
jogadores = json.loads(dados_json)

# Cria a pasta de destino igual ao caminho relativo do JSON (recria a estrutura public/)
pasta_destino = "public"
os.makedirs(pasta_destino, exist_ok=True)

print("Iniciando busca, crop (300x300) e salvamento baseado no JSON...")

with DDGS() as ddgs:
    for jogador in jogadores:
        nome = jogador["desc"]
        time_nba = jogador["team"]
        
        # Extrai o nome do arquivo final (ex: '../../public/bird.jpg' vira 'bird.jpg')
        nome_arquivo_original = os.path.basename(jogador["imagem"])
        caminho_final = os.path.join(pasta_destino, nome_arquivo_original)
        
        # Ignora se já existir
        if os.path.exists(caminho_final):
            print(f"[{nome}] Imagem '{nome_arquivo_original}' já existe. Pulando...")
            continue
            
        termo_busca = f"{nome} {time_nba} nba profile headshot"
        print(f"Buscando: {nome} ({time_nba})...")
        
        try:
            resultados = list(ddgs.images(termo_busca, max_results=1))
            
            if resultados:
                url_img = resultados[0]['image']
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
                resposta = requests.get(url_img, headers=headers, timeout=12)
                
                if resposta.status_code == 200:
                    img = Image.open(BytesIO(resposta.content)).convert("RGB")
                    
                    # Corta e redimensiona centralizando para 300x300
                    img_cropped = ImageOps.fit(img, (300, 300), method=Image.Resampling.LANCZOS)
                    
                    # Salva com o nome exato do JSON na pasta public/
                    img_cropped.save(caminho_final, "JPEG", quality=90)
                    print(f"✅ Salvo com sucesso: {caminho_final}")
                else:
                    print(f"❌ Erro HTTP {resposta.status_code} para {nome}")
            else:
                print(f"⚠️ Nenhuma imagem encontrada para {nome}")
                
        except Exception as e:
            print(f"⚠️ Falha ao processar {nome}: {e}")
            
        # Delay anti-block de 2 segundos
        time.sleep(2)

print("\nProcesso concluído com sucesso! Suas fotos 300x300 estão na pasta 'public'.")