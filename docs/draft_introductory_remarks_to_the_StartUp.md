В основу разработки нового продукта легла идея руководителя команды:
	вместо заурядного конструктора *Telegram*-ботов создать более
	универсальное решение, которое не только удовлетворяло бы самым актуальным запросам пользователей и
	обладало бы всеми преимуществами современного бизнес-инструмента,
	но ещё при этом было бы легкодоступным, простым и удобным в использовании даже для технически не очень подкованного пользователя,
	не смотря на высокий уровень сложности используемых при создании продукта передовых информационных технологий
	и методов их имплементации.

```
	Простота и удобство пользования продуктом - это требования из первоочередных к качественному продукту
на рынке высокотехнологичных бизнес-решений в реалиях сегодняшнего дня (современных условиях). 
```

​		Естественно, что в первую очередь даже профессиональный разработчик, как правило, обращает внимание на закладываемый в продукт функционал,
​	определяемый теми задачами (проблемами бизнеса), которые потребитель продукта (конечный пользователь или бизнес)
​	в конечном итоге сможет решать за счёт использования предоставленного ему продукта.
​	Чем шире предлагаемый функционал, тем от большего количества нерешённых задач поможет пользователю избавиться лишь этот один продукт,
​	то есть универсальность в немалой степени определяет выбор пользователя в пользу того или иного разрабатываемого решения,
​	а от выбора пользователя, конечно же, зависит успех и самого разработчика.
​	
​		Однако в современном мире в условиях жёсткой конкуренции, учитывая величайшее многообразие всевозможных представленных решений,
​	и разработку даже начинать необходимо с пониманием того, что продукт может стать интересен пользователю, когда он будет и нести в себе
​	богатый функционал, на данный момент ещё не представленный ни одним из имеющихся на рынке решений, и в то же время будет очень удобен и прост в использовании. 
​	
​		В реализации идеи создания сложного продукта, при использовании которого сложностей возникать не должно, решили идти от простого к сложному:
​	сперва создание простейшей модели *MVP* (англ. *Minimum Viable Product, MVP*) —
​	минимально жизнеспособный продукт — обладающий минимальными, но достаточными для удовлетворения первых потребителей функциями;
​	основная задача — получение обратной связи для формирования гипотез дальнейшего развития продукта,
​	такой подход зачастую позволяет снизить затраты и риски по сравнению с вариантом, когда разрабатывается продукт сразу с большим количеством функций.
​		Deadline для реализации *MVP* намечен на <u>15.12.2022</u> (спустя полтора месяца после начала работы над продуктом)
​	
​		Кроме того, при ориентированном на создание *MVP* подходе участники команды, пока ещё не обладающие серьёзным опытом в разработке,
​	смогут такой опыт приобрести,	решая элементарные задачи по созданию базового функционала и постепенно дополняя его новыми возможностями.
​		Команда небольшая:
​	всего 7 человек, включая руководителя -
​	Нурлан, Вячеслав (аналитик), Канат (junior python dev), Вадим (experienced backend dev), Шамиль (tech writer), Алексей(junior python dev), Еркожа (front-end dev)
​		
​		Нурлан будучи предприимчивым человеком, как мне видится, со множеством возникающих в ясной голове светлых мыслей 
​	поделился со всей нашей командой, предварительно самостоятельно создав её, одной из своих интересных идей,
​	вдохновляя на реализацию всем, что от него исходит, и давая проникнуться атмосферой успеха с самых первых часов знакомства
​	с этим человеком, открытым и внимательным к практически не знакомым окружающим его людям, которые даже находились ещё на огромном
​	расстоянии от города, где расположился новй офис только что созданной компании, оказавшись в котором ощущаешь уют и тепло.



​		Вячеслав как аналитик провёл предварительный анализ уже имеющихся на рынке решений с использованием чат-ботов,
​	акцент был сделан на сервисы построения *Telegram*-ботов.
​	Выделены три основных конкурента, определены основные преимущества,
​	которые мы будем стремиться заложить в разрабатываемый продукт; а также выделены недостатки, которые постараемся исключить
​	и минимизировать.
​	Проведённый обзор позволил сделать вывод о предполагаемой целевой аудитории разрпабатываемого сервиса:
​	преимущественную часть пользователей *Telegram*-ботов составляют *Online*-магазины (c долей в 77.4%), что предварительно ориентирует
​	смещение акцента в разработке основного функционала именно в сторону этого пользовательского сегмента.
​	
​		В качестве основного выделен следующий функционал:

- создание связей и сценариев ответов
- построение базы данных синонимов
- создание/хранение/редактирование/использование баз данных 
- сбор статистики и метрик
- обеспечение возможности использования готовых сценариев

В отношении каждого из приведённых функциональных направлений были рассмотрены примеры с разбором положительных и отрицательных сторон
реализованных конкурентами сервисов.


​	

​		Вячеслав, кроме решения задач аналитики, по согласованию с Нурланом параллельно занимался и другими вопросами:
​			1). разработка логотипа компании
​			2). приобретение соответствующего фирменному названию компании домена

​	Несколько слов о разработчиках в нашей команде.
​	Самый опытный специалист в нашей команде Вадим, получивший специализированное образование и длительное время занимавшийся коммерческой разработкой
в нескольких крупных компаниях. Вадим закончил Уфимский Государственный Авиационный Технический Университет по специальности "Вычислительные машины, системы, комплексы и сети".
В разработке более 10 лет, занимался промышленной разработкой приложений с использованием языка программирования C++ (framework Qt), Python, C#.
Основные языки разработки для него сейчас это Python и C#.

​	Канат (junior python dev) - в скором будущем выпускник кафедры компьютерных наук университета в городе Алматы;
5-й год учится по специальности "Вычислительная техника и программное обеспечение".
Коммерческий опыт начал получать ещё во время учёбы на 3-м курсе, занимаясь программной разработкой в банке Home Credit,
затем на четвёртом курсе в течение полугода продолжал программировать уже в банке Kaspi до начала дипломного проекта,
на протяжении 3-х месяцев параллельно с работой над дипломом получал опыт на позиции Project Manager'а;
научился писать код для проведения тестов, во время решения задач предыдущего startup-проекта проиобрёл опыт написания кода для создания Telegram-бота.

​	Шамиль наряду с инженерным образованием в сфере машиностроения, имея интерес к информационным технологиям ещё со школьной поры,
решил переквалифицироваться в IT-специалиста уже года 4 назад. Годового университетского курса по информатике, понятное дело, крайне
недостаточно для того, чтобы стать разработчиком, но полученные знания и приобретённый опыт позволяли комфортно себя ощущать в процессе
погружения в сферу IT посредством самостоятельного изучения: познакомился с основами работы со средой Linux, приобрёл пользовательский опыт по настройке Windows,
базовые знания по структуре и функционированию системы Android, изучил основы PHP, получил опыт установки LAMP-стека с предварительной подготовкой к работе с MySQL
(представление о работе с SQL, но без обширного практического опыта с SQL,
имею представление о применяемых в SQL запросах), также приобрёл опыт подготовки среды для работы с Anaconda, Jupyter Notebook в среде Linux.
Как направления интересны DevOps, автоматизация процессов, MLOps, Data Science, системы виртуализации и информационной безопасности, сетевые технологии.
​	В текущем start-up'е приступил к решению задач в роли технического писателя с намерением расширить общие познания в сфере информационных технологий,
перенять практический опыт разработки, более глубоко погрузиться в такие направления как Data Science и DevOps.
​	

​	Алексей закончил Аграрный университет в городе Санкт-Петербурге, направление "Менеджер по туризму", но по специальности так и работал; некоторое время был занят в сфере общепита в роли бармена. Затем долгое время проработал в компании, которая выполняла роль посредника между "РЖД" и сервисной компанией, непосредственно осуществляющей утилизацию железнодорожных вагонов. Через несколько лет работы в этой компании Алексея часто стали посещать мысли о смене рода деятельности, а именно хотелось заняться информационными технологиями. Очередная из неоднократных попыток пройти обучающие курсы в итоге принесли свой результат: Алексей успешно закончил курсы от "Яндекс практикума" по направлению *Python-разработчик* и уже спустя короткое время оказался в команде *"Cuttle Systems"*, приехав в казахстанский город Алматы. 

 	По проекту Алексей делает всё, что связано с framework'ом *Djungo* , развернул *Djungo*-проект, создал базовые *endpoint'ы:*

- получение, создание, изменение, удаление вариантов бота
- получение, создание, изменение, удаление сообщений
- получение, создание, изменение, удаление вариантов для сообщений



----------------------------------------------------------------------------------------------------------------------------------------------------------------

## Ниже вариант после корректирования Нурланом



​	Рады приветствовать вас на странице нового *startup*-проекта, посвященного разработке
универсального конструктора *Telegram*-ботов, способного легко вывести любой бизнес на
новый уровень!



**Идея нового продукта**

​	Основоположником разработки уникального продукта выступил руководитель нашей
команды – Нурлан. Он предложил вместо заурядного конструктора *Telegram*-ботов
создать более универсальное решение, которое будет соответствовать следующим
критериям:
• способность удовлетворять самым актуальным запросам пользователей;
• обладание всеми преимуществами современного бизнес-инструмента;
• легкодоступность для всех категорий пользователей;
• простота и удобство в использовании даже для технически не очень подкованного
пользователя.

​	Все это станет возможным, не смотря на высокий уровень сложности используемых при
создании продукта передовых информационных технологий и методов их имплементации.



**Задачи продукта**

​	При разработке конструктора Telegram-ботов главная задача состоит в обеспечении
простоты и удобства пользования продуктом. По нашему мнению, действительно
качественный продукт на рынке высокотехнологичных бизнес-решений в современных
реалиях должен в первую очередь отвечать именно этому требованию.

​	Второй нашей задачей выступает обеспечение универсальности закладываемого в продукт
функционала. Он будет определяться теми задачами и проблемами бизнеса, которые
потребитель продукта в конечном итоге сможет решать за счет использования
предоставленного ему конструктора. Любой профессиональный разработчик должен
ставить задачей своей разработки решение проблем клиента, поэтому наш продукт будет
нацелен на достижение этой цели.
​	Поскольку наша задача заключается в создании универсального решения, функционал
конструктора будет максимально расширен. Чем шире предлагаемый функционал, тем от
большего количества нерешенных задач поможет пользователю избавиться лишь один
продукт.

​	Таким образом универсальность в немалой степени определяет выбор
пользователя в пользу того или иного разрабатываемого решения, а от выбора
пользователя, безусловно, зависит успех и самого разработчика.
​	Современный рынок отличается величайшим многообразием всевозможных предложений
и жесткой конкуренцией. Именно поэтому разработку необходимо начинать с
пониманием того, что продукт может стать интересен пользователю, если он будет и
нести в себе богатый функционал, на данный момент еще не представленный ни одним из
имеющихся на рынке решений, и в то же время будет очень удобен и прост в
использовании.



**Этапы реализации проекта**

​	В основе идеи лежит создание сложного продукта, при использовании которого
трудностей возникать не должно. Мы решили идти от простого к сложному, поэтому
этапы разработки выглядят таким образом:

1. Создание простейшей модели *MVP (англ. Minimum Viable Product, MVP)*

2. Создание минимально жизнеспособного продукта, обладающего минимальными,
   но достаточными для удовлетворения первых потребителей функциями

3. Получение обратной связи для формирования гипотез дальнейшего развития
   продукта

   

   ​	Получение обратной связи от пользователей является основной задачей на данном этапе разработки. Такой подход позволит снизить затраты и риски по сравнению с вариантом, когда разрабатывается продукт сразу с большим количеством функций.
   Кроме того, при ориентированном на создание *MVP* подходе участники команды смогут
   приобрести дополнительный опыт в разработке, решая элементарные задачи по созданию
   базового функционала и постепенно дополняя его новыми возможностями, а также
   предложить наиболее оптимальное решение, лишенное большинства недостатков.
   Deadline для реализации MVP намечен на 15 декабря 2022 года – спустя полтора месяца после начала работы над продуктом.

   

   **История создания и проведенная работа**

   ​	Наша компания *Cuttle Systems* была создана предприимчивым человеком с множеством
   возникающих в ясной голове светлых мыслей – Нурланом. Некоторые члены команды
   находились на огромном расстоянии от города, в котором расположился новый офис
   только что созданной компании. Однако открытость, нацеленность на результат и
   внимательность даже к практически не знакомым окружающим людям смогли сплотить
   нас и воодушевить на плодотворную работу. Оказавшись в офисе *Cuttle Systems*, сразу
   ощущаешь уют, тепло и желание творить.
   ​	Интересная идея Нурлана вдохновила нас на реализацию действительно востребованного продукта и буквально заразила уверенностью и здравым азартом. С самых первых часов взаимодействия в компании мы прониклись атмосферой успеха и уверенности в перспективности нашего продукта.
   ​	Вячеслав как аналитик провел предварительный анализ уже имеющихся на рынке
   решений с использованием чат-ботов, сделав акцент на сервисы построения *Telegram*-
   ботов.
   ​	В ходе аналитической работы были выделены три основный конкурента и определены
   главные преимущества, которые мы будем стремиться заложить в разрабатываемый
   продукт, а также недостатки, которые постараемся исключить или минимизировать.

   ​	По согласованию с Нурланом, кроме решения задач аналитики, Вячеслав параллельно
   занимался и другими вопросами:
   • разработка логотипа компании;
   • приобретение соответствующего фирменному названию компании домена.

   

   **Целевая аудитория**

   ​	Проведенный обзор позволил нам сделать вывод о предполагаемой целевой аудитории
   разрабатываемого сервиса. Поскольку преимущественную часть пользователей *Telegram*-
   ботов составляют *Online*-магазины (c долей в 77.4%), мы сместили акцент в разработке
   основного функционала именно в сторону этого пользовательского сегмента.

   

   В качестве основного был выделен следующий функционал:
   • создание связей и сценариев ответов;
   • построение базы данных синонимов;
   • создание/хранение/редактирование/использование баз данных;
   • сбор статистики и метрик;
   • обеспечение возможности использования готовых сценариев.
   В отношении каждого из приведенных функциональных направлений были рассмотрены
   примеры с разбором положительных и отрицательных сторон реализованных
   конкурентами сервисов.

   

   **Разработчики в нашей команде**

   ​	В состав нашей небольшой команды входят 7 человек:

   1. Нурлан – руководитель
   2. Вячеслав – аналитик
   3. Канат – junior python dev
   4. Вадим – experienced dev
   5. Шамиль – tech writer
   6. Алексей – junior python dev
   7. Еркожа – front-end dev

   

   ​	Самый опытный специалист в нашей команде – Вадим, получивший специализированное
   образование и длительное время занимавшийся коммерческой разработкой в нескольких крупных компаниях. Вадим закончил Уфимский Государственный Авиационный Технический Университет по специальности «Вычислительные машины, системы, комплексы и сети». В разработке Вадим более 10 лет, занимался промышленной разработкой приложений с использованием языка программирования *C++*, *Python*, *C#*.
   ​	Основные языки разработки для него сейчас – это *Python* и *C#*.
   
   	Шамиль наряду с инженерным образованием в сфере машиностроения, имея интерес к информационным технологиям еще со школьной поры, 4 назад года решил
   переквалифицироваться в *IT*-специалиста. Не смотря на то, что годового университетского курса по информатике недостаточно, чтобы стать разработчиком, полученные знания и приобретенный опыт позволили ему комфортно себя ощущать в процессе погружения в сферу *IT* посредством самостоятельного изучения, в чем он весьма преуспел. Как направления ему интересны *DevOps*, автоматизация процессов, системы виртуализации и информационной безопасности и сетевые технологии.
   	В текущем start-up'е Шамиль приступил к решению задач в роли технического писателя с намерением расширить общие познания в сфере информационных технологий, перенять практический опыт разработки и глубже погрузиться в такие направления, как *Data Science* и *DevOps*.

   ​	Алексей и Еркожа, имея навыки работы в *IT*-сфере и необходимую подготовку, также принимают активное участие в создании нового продукта.
   ​	Мы намерены создать действительно уникальный продукт и будем регулярно
   анонсировать информацию о ходе нашей разработки. Следите за нашими новостями –
   уверены, это будет очень интересно!

