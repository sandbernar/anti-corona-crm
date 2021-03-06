all_regions = "Все Регионы"
hospitals_list_xlsx = "app/data/hospitals_list.xlsx"
all_hospital_types = "Все Типы"
all_hospital_nomenklatura = "Все Номенклатуры"
no_hospital = "Не Госпитализирован"
hospital_additional_types = ["другое"]

current_country = "KZ"

# Flight Code
all_flight_codes = "Все Рейсы"

# patient_statuses = [no_status, in_hospital, is_home, is_transit]

# Regions
out_of_rk = "Вне РК"

# Travel Type
all_travel_types = ("all_travel_types", "Все Типы")
train_type = ("train_type", "Поезд")
by_auto_type = ("auto_type", "Авто")
by_foot_type = ("by_foot", "Пешком")
by_sea_type = ("by_sea", "Морской Транспорт")
flight_type = ("flight_type", "Самолет")
local_type = ("local_type", "Местные")
blockpost_type = ("blockpost_type", "Блокпост")
old_data_type = ("old_data_type", "Старые Данные")

all_blockposts = (-1, "Все Блокпосты")
all_dates = (-1, "Все Даты")

various_travel_types = [by_auto_type, by_foot_type, by_sea_type]
various_travel_types_values = [val[0] for val in various_travel_types]

board_team = "экипаж"

travel_types = [flight_type, train_type, by_auto_type, by_foot_type, by_sea_type, local_type, old_data_type, blockpost_type]

unknown = (None, "Неизвестно")

kz_center_lat_lng = (48.191216, 68.883269)

# Job Categories
all_job_categories = (-1, "Все Категории")
doctors_job_category = ("doctors_job_category", "Врач")
police_job_category = ("police_job_category", "Полицейский")
military_job_category = ("military_job_category", "Военный")

job_categories = [doctors_job_category, police_job_category, military_job_category]

cyrillic_to_ascii = {
    "А": "A",
    "Б": "B",
    "В": "B",
    "Г": "G",
    "Д": "D",
    "Е": "E",
    "К": "K",
    "Н": "H",
    "М": "M",
    "С": "C",
    "Х": "X",
    "Т": "T"
}

# Address Location Types
unknown_loc_type = (-1, "Неизвестно")
village_loc_type = ("village_loc_type", "Село")
city_loc_type = ("city_loc_type", "Город")

address_loc_types = [village_loc_type, city_loc_type]

# Countries
country_category = ["1a", "1b", "2", "3", "4"]

by_earth_border = ['Айша-биби', 'Акбалшык', 'Аксай', 'Алаколь', 'Алимбет',
       'Аманкелди', 'Атакент', 'Атамекен', 'Аухатты', 'Ауыл', 'Аят',
       'Б.Конысбаева', 'Байтанат', 'Бахты', 'Бидаик', 'Достык', 'Жайсан',
       'Жана-Жол', 'Жаныбек', 'Жезкент', 'Желкуар', 'Жибек-Жолы',
       'Казыгурт', 'Кайрак', 'Калжат', 'Капланбек', 'Каракога', 'Карасу',
       'Карашатау', 'Кеген', 'Кондыбай', 'Коргас (Хоргос)', 'Кордай',
       'Косак', 'Коянбай', 'Курмангазы', 'Кызыл Жар', 'Майкапчагай',
       'Найза', 'Нуржолы', 'Орал', 'Сайхин ', 'Сартобе', 'Сыпатай Батыр',
       'Сырым', 'Тажен', 'Таскала', 'Темир-баба', 'Убаган', 'Убе',
       'Урлитобе', 'Целинный', 'Шарбакты']

by_sea_border = ['Актау Морпорт', 'Курык Морпорт']

code_country_list = [("AU", "Австралия"),
                    ("AT", "Австрия"),
                    ("AZ", "Азербайджан"),
                    ("AX", "Аландские о-ва"),
                    ("AL", "Албания")	,
                    ("DZ", "Алжир"),
                    ("AS", "Американское Самоа"),
                    ("AI", "Ангилья"),
                    ("AO", "Ангола"),
                    ("AD", "Андорра"),
                    ("AQ", "Антарктида"),
                    ("AG", "Антигуа и Барбуда"),
                    ("AR", "Аргентина"),
                    ("AM", "Армения"),
                    ("AW", "Аруба"),
                    ("AF", "Афганистан"),
                    ("BS", "Багамы"),
                    ("BD", "Бангладеш"),
                    ("BB", "Барбадос"),
                    ("BH", "Бахрейн"),
                    ("BY", "Беларусь"),
                    ("BZ", "Белиз"),
                    ("BE", "Бельгия"),
                    ("BJ", "Бенин"),
                    ("BM", "Бермудские о-ва"),
                    ("BG", "Болгария"),
                    ("BO", "Боливия"),
                    ("BQ", "Бонэйр, Синт-Эстатиус и Саба"),
                    ("BA", "Босния и Герцеговина"),
                    ("BW", "Ботсвана"),
                    ("BR", "Бразилия"),
                    ("IO", "Британская территория в Индийском океане"),
                    ("BN", "Бруней-Даруссалам"),
                    ("BF", "Буркина-Фасо"),
                    ("BI", "Бурунди"),
                    ("BT", "Бутан"),
                    ("VU", "Вануату"),
                    ("VA", "Ватикан"),
                    ("GB", "Великобритания"),
                    ("HU", "Венгрия"),
                    ("VE", "Венесуэла"),
                    ("VG", "Виргинские о-ва (Великобритания)"),
                    ("VI", "Виргинские о-ва (США)"),
                    ("UM", "Внешние малые о-ва (США)"),
                    ("TL", "Восточный Тимор"),
                    ("VN", "Вьетнам"),
                    ("GA", "Габон"),
                    ("HT", "Гаити"),
                    ("GY", "Гайана"),
                    ("GM", "Гамбия"),
                    ("GH", "Гана"),
                    ("GP", "Гваделупа"),
                    ("GT", "Гватемала"),
                    ("GN", "Гвинея"),
                    ("GW", "Гвинея-Бисау"),
                    ("DE", "Германия"),
                    ("GG", "Гернси"),
                    ("GI", "Гибралтар"),
                    ("HN", "Гондурас"),
                    ("HK", "Гонконг (САР)"),
                    ("GD", "Гренада"),
                    ("GL", "Гренландия"),
                    ("GR", "Греция"),
                    ("GE", "Грузия"),
                    ("GU", "Гуам"),
                    ("DK", "Дания"),
                    ("JE", "Джерси"),
                    ("DJ", "Джибути"),
                    ("DG", "Диего-Гарсия"),
                    ("DM", "Доминика"),
                    ("DO", "Доминиканская Республика"),
                    ("EG", "Египет"),
                    ("ZM", "Замбия"),
                    ("EH", "Западная Сахара"),
                    ("ZW", "Зимбабве"),
                    ("IL", "Израиль"),
                    ("IN", "Индия"),
                    ("ID", "Индонезия"),
                    ("JO", "Иордания"),
                    ("IQ", "Ирак"),
                    ("IR", "Иран"),
                    ("IE", "Ирландия"),
                    ("IS", "Исландия"),
                    ("ES", "Испания"),
                    ("IT", "Италия"),
                    ("YE", "Йемен"),
                    ("CV", "Кабо-Верде"),
                    ("KZ", "Казахстан"),
                    ("KH", "Камбоджа"),
                    ("CM", "Камерун"),
                    ("CA", "Канада"),
                    ("IC", "Канарские о-ва"),
                    ("QA", "Катар"),
                    ("KE", "Кения"),
                    ("CY", "Кипр"),
                    ("KG", "Киргизия"),
                    ("KI", "Кирибати"),
                    ("CN", "Китай"),
                    ("KP", "КНДР"),
                    ("CC", "Кокосовые о-ва"),
                    ("CO", "Колумбия"),
                    ("KM", "Коморы"),
                    ("CG", "Конго - Браззавиль"),
                    ("CD", "Конго - Киншаса"),
                    ("XK", "Косово"),
                    ("CR", "Коста-Рика"),
                    ("CI", "Кот-д&rsquo;Ивуар"),
                    ("CU", "Куба"),
                    ("KW", "Кувейт"),
                    ("CW", "Кюрасао"),
                    ("LA", "Лаос"),
                    ("LV", "Латвия"),
                    ("LS", "Лесото"),
                    ("LR", "Либерия"),
                    ("LB", "Ливан"),
                    ("LY", "Ливия"),
                    ("LT", "Литва"),
                    ("LI", "Лихтенштейн"),
                    ("LU", "Люксембург"),
                    ("MU", "Маврикий"),
                    ("MR", "Мавритания"),
                    ("MG", "Мадагаскар"),
                    ("YT", "Майотта"),
                    ("MO", "Макао (САР)"),
                    ("MW", "Малави"),
                    ("MY", "Малайзия"),
                    ("ML", "Мали"),
                    ("MV", "Мальдивы"),
                    ("MT", "Мальта"),
                    ("MA", "Марокко"),
                    ("MQ", "Мартиника"),
                    ("MH", "Маршалловы Острова"),
                    ("MX", "Мексика"),
                    ("MZ", "Мозамбик"),
                    ("MD", "Молдова"),
                    ("MC", "Монако"),
                    ("MN", "Монголия"),
                    ("MS", "Монтсеррат"),
                    ("MM", "Мьянма (Бирма)"),
                    ("NA", "Намибия"),
                    ("NR", "Науру"),
                    ("NP", "Непал"),
                    ("NE", "Нигер"),
                    ("NG", "Нигерия"),
                    ("NL", "Нидерланды"),
                    ("NI", "Никарагуа"),
                    ("NU", "Ниуэ"),
                    ("NZ", "Новая Зеландия"),
                    ("NC", "Новая Каледония"),
                    ("NO", "Норвегия"),
                    ("AC", "о-в Вознесения"),
                    ("IM", "о-в Мэн"),
                    ("NF", "о-в Норфолк"),
                    ("CX", "о-в Рождества"),
                    ("SH", "о-в Св. Елены"),
                    ("PN", "о-ва Питкэрн"),
                    ("TC", "о-ва Тёркс и Кайкос"),
                    ("AE", "ОАЭ"),
                    ("OM", "Оман"),
                    ("KY", "Острова Кайман"),
                    ("CK", "Острова Кука"),
                    ("PK", "Пакистан"),
                    ("PW", "Палау"),
                    ("PS", "Палестинские территории"),
                    ("PA", "Панама"),
                    ("PG", "Папуа &mdash; Новая Гвинея"),
                    ("PY", "Парагвай"),
                    ("PE", "Перу"),
                    ("PL", "Польша"),
                    ("PT", "Португалия"),
                    ("XB", "псевдо-Bidi"),
                    ("XA", "псевдоакценты"),
                    ("PR", "Пуэрто-Рико"),
                    ("KR", "Республика Корея"),
                    ("RE", "Реюньон"),
                    ("RU", "Россия"),
                    ("RW", "Руанда"),
                    ("RO", "Румыния"),
                    ("SV", "Сальвадор"),
                    ("WS", "Самоа"),
                    ("SM", "Сан-Марино"),
                    ("ST", "Сан-Томе и Принсипи"),
                    ("SA", "Саудовская Аравия"),
                    ("MK", "Северная Македония"),
                    ("MP", "Северные Марианские о-ва"),
                    ("SC", "Сейшельские Острова"),
                    ("BL", "Сен-Бартелеми"),
                    ("MF", "Сен-Мартен"),
                    ("PM", "Сен-Пьер и Микелон"),
                    ("SN", "Сенегал"),
                    ("VC", "Сент-Винсент и Гренадины"),
                    ("KN", "Сент-Китс и Невис"),
                    ("LC", "Сент-Люсия"),
                    ("RS", "Сербия"),
                    ("EA", "Сеута и Мелилья"),
                    ("SG", "Сингапур"),
                    ("SX", "Синт-Мартен"),
                    ("SY", "Сирия"),
                    ("SK", "Словакия"),
                    ("SI", "Словения"),
                    ("US", "Соединенные Штаты"),
                    ("SB", "Соломоновы Острова"),
                    ("SO", "Сомали"),
                    ("SD", "Судан"),
                    ("SR", "Суринам"),
                    ("SL", "Сьерра-Леоне"),
                    ("TJ", "Таджикистан"),
                    ("TH", "Таиланд"),
                    ("TW", "Тайвань"),
                    ("TZ", "Танзания"),
                    ("TG", "Того"),
                    ("TK", "Токелау"),
                    ("TO", "Тонга"),
                    ("TT", "Тринидад и Тобаго"),
                    ("TA", "Тристан-да-Кунья"),
                    ("TV", "Тувалу"),
                    ("TN", "Тунис"),
                    ("TM", "Туркменистан"),
                    ("TR", "Турция"),
                    ("UG", "Уганда"),
                    ("UZ", "Узбекистан"),
                    ("UA", "Украина"),
                    ("WF", "Уоллис и Футуна"),
                    ("UY", "Уругвай"),
                    ("FO", "Фарерские о-ва"),
                    ("FM", "Федеративные Штаты Микронезии"),
                    ("FJ", "Фиджи"),
                    ("PH", "Филиппины"),
                    ("FI", "Финляндия"),
                    ("FK", "Фолклендские о-ва"),
                    ("FR", "Франция"),
                    ("GF", "Французская Гвиана"),
                    ("PF", "Французская Полинезия"),
                    ("TF", "Французские Южные территории"),
                    ("HR", "Хорватия"),
                    ("CF", "Центрально-Африканская Республика"),
                    ("TD", "Чад"),
                    ("ME", "Черногория"),
                    ("CZ", "Чехия"),
                    ("CL", "Чили"),
                    ("CH", "Швейцария"),
                    ("SE", "Швеция"),
                    ("SJ", "Шпицберген и Ян-Майен"),
                    ("LK", "Шри-Ланка"),
                    ("EC", "Эквадор"),
                    ("GQ", "Экваториальная Гвинея"),
                    ("ER", "Эритрея"),
                    ("SZ", "Эсватини"),
                    ("EE", "Эстония"),
                    ("ET", "Эфиопия"),
                    ("GS", "Южная Георгия и Южные Сандвичевы о-ва"),
                    ("ZA", "Южно-Африканская Республика"),
                    ("SS", "Южный Судан"),
                    ("JM", "Ямайка"),
                    ("JP", "Япония")]

HGDBCountry = {
    "6":"Азербайджан",
    "16":"Армения",
    "85":"Казахстан",
    "166":"Российская федерация",
    "1001":"Не указано",
    "1002":"Острова Питкэрн",
    "1003":"Шпицберген и Ян-Майен",
    "1004":"Австралия",
    "1005":"Австрия",
    "1006":"Азербайджан",
    "1007":"Албания",
    "1008":"Алжир",
    "1009":"Американское Самоа",
    "1010":"Ангилья",
    "1011":"Ангола",
    "1012":"Андорра",
    "1013":"Антарктида",
    "1014":"Антигуа и Барбуда",
    "1015":"Аргентина",
    "1016":"Армения",
    "1017":"Аруба",
    "1018":"Афганистан",
    "1019":"Багамы",
    "1020":"Бангладеш",
    "1021":"Барбадос",
    "1022":"Бахрейн",
    "1023":"Белоруссия",
    "1024":"Белиз",
    "1025":"Бельгия",
    "1026":"Бенин",
    "1027":"Бермуды",
    "1028":"Болгария",
    "1029":"Боливия",
    "1030":"Босния и Герцеговина",
    "1031":"Ботсвана",
    "1032":"Бразилия",
    "1033":"Британская территория в Индийском океане",
    "1034":"Бруней",
    "1035":"Буркина-Фасо",
    "1036":"Бурунди",
    "1037":"Бутан",
    "1038":"Вануату",
    "1039":"Ватикан",
    "1040":"Венгрия",
    "1041":"Венесуэла",
    "1042":"Виргинские Острова (Великобритания)",
    "1043":"Виргинские Острова (США)",
    "1044":"Восточный Тимор",
    "1045":"Вьетнам",
    "1046":"Габон",
    "1047":"Гаити",
    "1048":"Гайана",
    "1049":"Гамбия",
    "1050":"Гана",
    "1051":"Гваделупа",
    "1052":"Гватемала",
    "1053":"Гвинея",
    "1054":"Гвинея-Бисау",
    "1055":"Германия",
    "1056":"Гибралтар",
    "1057":"Гонконг",
    "1058":"Гондурас",
    "1059":"Гренада",
    "1060":"Гренландия",
    "1061":"Греция",
    "1062":"Грузия",
    "1063":"Гуам",
    "1064":"Дания",
    "1065":"Джибути",
    "1066":"Доминика",
    "1067":"Доминиканская Республика",
    "1068":"Египет",
    "1069":"Демократическая Республика Конго",
    "1070":"Замбия",
    "1071":"САДР",
    "1072":"Зимбабве",
    "1073":"Израиль",
    "1074":"Индия",
    "1075":"Индонезия",
    "1076":"Иордания",
    "1077":"Ирак",
    "1078":"Иран",
    "1079":"Ирландия",
    "1080":"Исландия",
    "1081":"Испания",
    "1082":"Италия",
    "1083":"Йемен",
    "1084":"Кабо-Верде",
    "1085":"Казахстан",
    "1086":"Острова Кайман",
    "1087":"Камбоджа",
    "1088":"Камерун",
    "1089":"Канада",
    "1090":"Катар",
    "1091":"Кения",
    "1092":"Кипр",
    "1093":"Кирибати",
    "1094":"КНР (Китайская Народная Республика)",
    "1095":"Кокосовые острова",
    "1096":"Колумбия",
    "1097":"Коморы",
    "1098":"Республика Конго",
    "1099":"КНДР (Корейская Народно-Демократическая Республика)",
    "1100":"Республика Корея",
    "1101":"Коста-Рика",
    "1102":"Кот-д’Ивуар",
    "1103":"Куба",
    "1104":"Кувейт",
    "1105":"Киргизия",
    "1106":"Лаос",
    "1107":"Латвия",
    "1108":"Лесото",
    "1109":"Либерия",
    "1110":"Ливан",
    "1111":"Ливия",
    "1112":"Литва",
    "1113":"Лихтенштейн",
    "1114":"Люксембург",
    "1115":"Маврикий",
    "1116":"Мавритания",
    "1117":"Мадагаскар",
    "1118":"Майотта",
    "1119":"Макао",
    "1120":"Македония",
    "1121":"Малави",
    "1122":"Малайзия",
    "1123":"Мали",
    "1124":"Мальдивы",
    "1125":"Мальта",
    "1126":"Марокко",
    "1127":"Мартиника",
    "1128":"Маршалловы Острова",
    "1129":"Мексика",
    "1130":"Микронезия",
    "1131":"Мозамбик",
    "1132":"Молдавия",
    "1133":"Монако",
    "1134":"Монголия",
    "1135":"Монтсеррат",
    "1136":"Намибия",
    "1137":"Науру",
    "1138":"Непал",
    "1139":"Нигер",
    "1140":"Нигерия",
    "1141":"Нидерландские антилы",
    "1142":"Нидерланды",
    "1143":"Никарагуа",
    "1144":"Ниуэ",
    "1145":"Новая Зеландия",
    "1146":"Новая Каледония",
    "1147":"Норвегия",
    "1148":"Остров Норфолк",
    "1149":"Ньянмар (бирма)",
    "1150":"ОАЭ",
    "1151":"Оман",
    "1152":"Херд и Макдональд",
    "1153":"Остров Буве",
    "1154":"Острова Кука",
    "1155":"Пакистан",
    "1156":"Палау",
    "1157":"Панама",
    "1158":"Папуа — Новая Гвинея",
    "1159":"Парагвай",
    "1160":"Перу",
    "1161":"Польша",
    "1162":"Португалия",
    "1163":"Пуэрто-Рико",
    "1164":"Реюньон",
    "1165":"Остров Рождества",
    "1166":"Россия",
    "1167":"Руанда",
    "1168":"Румыния",
    "1169":"Самоа",
    "1170":"Сан-Марино",
    "1171":"Сан-Томе и Принсипи",
    "1172":"Саудовская Аравия",
    "1173":"Острова Святой Елены, Вознесения и Тристан-да-Кунья",
    "1174":"Свазиленд",
    "1175":"Северные Марианские Острова",
    "1176":"Сейшельские Острова",
    "1177":"Сенегал",
    "1178":"Сен-Пьер и Микелон",
    "1179":"Сент-Винсент и Гренадины",
    "1180":"Сент-Китс и Невис",
    "1181":"Сент-Люсия",
    "1182":"Сингапур",
    "1183":"Сирия",
    "1184":"Словакия",
    "1185":"Словения",
    "1186":"Великобритания",
    "1187":"США",
    "1188":"Соединённые штаты без островов",
    "1189":"Соломоновы Острова",
    "1190":"Сомали",
    "1191":"Судан",
    "1192":"Суринам",
    "1193":"Сьерра-Леоне",
    "1194":"Таджикистан",
    "1195":"Таиланд",
    "1196":"Тайвань",
    "1197":"Танзания",
    "1198":"Тёркс и Кайкос",
    "1199":"Того",
    "1200":"Токелау",
    "1201":"Тонга",
    "1202":"Тринидад и Тобаго",
    "1203":"Тувалу",
    "1204":"Тунис",
    "1205":"Туркмения",
    "1206":"Турция",
    "1207":"Уганда",
    "1208":"Узбекистан",
    "1209":"Украина",
    "1210":"Уоллис и Футуна",
    "1211":"Уругвай",
    "1212":"Фареры",
    "1213":"Фиджи",
    "1214":"Филиппины",
    "1215":"Финляндия",
    "1216":"Фолклендские острова",
    "1217":"Франция",
    "1218":"Франция, метрополия",
    "1219":"Французская Гвиана",
    "1220":"Французская Полинезия",
    "1221":"Французские Южные и Антарктические Территории",
    "1222":"Хорватия",
    "1223":"Центрально-Африканская Республика",
    "1224":"Чад",
    "1225":"Чехия",
    "1226":"Чили",
    "1227":"Швейцария",
    "1228":"Швеция",
    "1229":"Шри-Ланка",
    "1230":"Эквадор",
    "1231":"Экваториальная Гвинея",
    "1232":"Сальвадор",
    "1233":"Эритрея",
    "1234":"Эстония",
    "1235":"Эфиопия",
    "1236":"Югославия",
    "1237":"ЮАР",
    "1238":"Южная Георгия и Южные Сандвичевы Острова",
    "1239":"Ямайка",
    "1240":"Япония",
    "1241":"Антильские острова",
    "1242":"Джонстона, остров",
    "1243":"Канала, острова",
    "1244":"Остров Мэн",
    "1245":"Мидуэй",
    "1246":"Мьянма",
    "1247":"Государство Палестина",
    "1248":"Свальбарда, остров",
    "1249":"Внешние малые острова (США)",
    "1250":"Уэйк",
    "1251":"Лицо без гражданства",
    "1252":"Черногория",
    "1253":"Сербия",
    "1254":"Аландские острова",
    "1255":"Бонэйр, Синт-Эстатиус и Саба",
    "1256":"Гернси",
    "1257":"Джерси",
    "1258":"Кюрасао",
    "1259":"Сен-Мартен",
    "1260":"Синт-Мартен (нидерландская часть)",
    "1261":"Сен-Бартелеми",
    "1262":"Китайская Республика",
    "1263":"Южный Судан",
    "1264":"Заграница"
}

# State
in_hospital = ("hospitalized", "Госпитализирован")

state_dead = ("dead", "Умер")
state_infec = ("infected", "Инфицирован")
state_hosp = ("hospitalized", "Госпитализирован")
state_hosp_off = ("hospitalized_off", "Госпитализирован - Выписка")

state_healthy = ("recovery", "Выздоровление")

state_is_home = ("is_home", "Домашний Карантин")
state_is_home_off = ("is_home_off", "Домашний Карантин - Окончание")

state_is_transit = ("transit", "Транзит")
state_found = ("found", "Найден")
states = [
    state_dead,
    state_infec,
    state_hosp,
    state_hosp_off,
    state_healthy,
    state_is_home,
    state_is_home_off,
    state_is_transit,
    state_found
]

form_states = [
    ("", ""),
    state_is_transit,
    state_hosp,
    state_is_home
]

unknown_num = ('-1', "Неизвестно")
all_types = ('-1', "Все")

all_types_none = (None, 'Все')

# state_infec
# Infection Types
self_request = ("self_request", "Самообращение")
prof_tzel = ("prof_tzel", "Проф. Цель")
zavoznoi = ("zavoznoi", "Завозной")

contacted_self_request = ("contacted_self_request", "Контактный Самообращение")
contacted_prof_tzel = ("contacted_prof_tzel", "Контактный  Проф. Цель")
contacted_zavoznoi = ("contacted_zavoznoi", "Контактный  Завозной")

state_infec_types = [unknown_num, self_request, prof_tzel, zavoznoi, contacted_self_request, contacted_prof_tzel, contacted_zavoznoi]

# Illness Symptoms
without_symptoms = ("without_symptoms", "Бессимптомно")
with_symptoms = ("with_symptoms", "Симптомно")

illness_symptoms = [unknown_num, without_symptoms, with_symptoms]

# Illness Severity
low_severity = ("low_severity", "Легкое")
medium_severity = ("medium_severity", "Среднее")
hard_severity = ("hard_severity", "Тяжёлое (критическое)")

illness_severity = [unknown_num, low_severity, medium_severity, hard_severity]

#state_dead
due_covid = ("due_covid", "От КВИ")
due_other = ("due_other", "От Сопутствующих")

death_reasons = [unknown_num, due_covid, due_other]

# Roles
skp_avia = ("skp_avia", "СКП (Авиа)")
skp_train = ("skp_train", "СКП (ЖД)")
skp_border_control = ("skp_border_control", "СКП (Только Граница)")
skp_blockpost = ("skp_blockpost", "СКП (Блокпост)")
epid = ("epid", "Эпидемиолог")
manager = ("manager", "Менеджер")
admin = ("admin", "Администратор")

roles = [skp_avia, skp_train, skp_border_control, skp_blockpost, epid, manager, admin]

class GraphNode:
    def __init__(self, value):
        self.value = value
        self.nodes = []
    
    def connect(self, node):
        self.nodes.append(node)

class GraphState:
    def __init__(self):
        self.start = GraphNode(1)
        self.reached_end = False
        self.location = []
        self.patient = []
        self.location_state = [state_found[0], state_is_transit[0], state_hosp[0], state_hosp_off[0], state_is_home[0], state_is_home_off[0]]
        self.patient_state = [state_found[0], state_infec[0], state_healthy[0], state_dead[0]]

        self.dead = GraphNode(state_dead)
        self.infec = GraphNode(state_infec)
        
        self.hosp = GraphNode(state_hosp)
        self.state_hosp_off = GraphNode(state_hosp_off)
        
        self.healthy = GraphNode(state_healthy)
        
        self.is_home = GraphNode(state_is_home)
        self.state_is_home_off = GraphNode(state_is_home_off)

        self.is_transit = GraphNode(state_is_transit)
        self.found = GraphNode(state_found)

        self.start.connect(self.found)
        self.found.connect(self.infec)
        self.found.connect(self.dead)
        self.found.connect(self.is_transit)
        self.found.connect(self.is_home)
        self.found.connect(self.hosp)
        self.is_transit.connect(self.hosp)
        self.is_transit.connect(self.is_home)
        
        self.is_home.connect(self.hosp)
        self.is_home.connect(self.healthy)
        self.is_home.connect(self.state_is_home_off)

        self.state_is_home_off.connect(self.is_home)
        self.state_is_home_off.connect(self.hosp)
        
        self.hosp.connect(self.is_home)
        self.hosp.connect(self.healthy)
        self.hosp.connect(self.state_hosp_off)
        
        self.state_hosp_off.connect(self.hosp)
        self.state_hosp_off.connect(self.is_home)

        self.infec.connect(self.healthy)
        self.infec.connect(self.dead)
        self.healthy.connect(self.infec)
        self.healthy.connect(self.dead)

        self.states = []
    
    def add(self, in_state):
        def checkStates(states):
            currentNode = self.start
            for state in states:
                found = False
                for node in currentNode.nodes:
                    if node.value[0] == state[0]:
                        currentNode = node
                        found = True
                        if node == self.dead:
                            self.reached_end = True
                        break
                if not found:
                    states.pop()
                    return False
            return True

        if self.reached_end:
            return False
        states = None
        if in_state[0] in self.location_state:
            states = self.location
        elif in_state[0] in self.patient_state:
            states = self.patient
        
        if in_state[0] in [state_found[0]]:
            self.location.append(in_state)
            self.patient.append(in_state)
            loc = checkStates(self.location)
            pat = checkStates(self.patient)
            return loc or pat
        states.append(in_state)
        return checkStates(states)
