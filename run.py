# Script de lancement de l'application
# run.py
from datetime import datetime
from app import create_app, db
from app.models import User, Artwork, Emotion, Vote, Comment, Report, Notification, Like

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        # Créer les tables si elles n'existent pas
        db.create_all()
        
        # Vérifier si la table User est vide
        if User.query.count() == 0:
            # Recréer les tables User, Emotion, et Artwork avec les données exactes
            # Table User
            users = [
                {"id": 1, "username": "olivier_richard", "email": "gbonourichard44@gmail.com", "password_hash": "Oliviertyui2004",
                "bio": "Adminstrateur de Gallerium. Passionné d'art comptemporain.", "avatar": "avatar0.jpg", "is_admin": True},
                {"id": 2, "username": "julie_peintre", "email": "julie.peintre@example.com", "password_hash": "Password123",
                "bio": "Passionnée de peinture impressionniste, j'aime capturer la lumière.", "avatar": "avatar1.jpg", "is_admin": False},
                {"id": 3, "username": "marc_artiste", "email": "marc.artiste@example.com", "password_hash": "Password123",
                "bio": "Sculpteur amateur, inspiré par la nature et les formes organiques.", "avatar": "avatar2.jpg", "is_admin": False},
                {"id": 4, "username": "sophie_dessin", "email": "sophie.dessin@example.com", "password_hash": "Password123",
                "bio": "Dessinatrice de portraits, toujours à la recherche d'émotions.", "avatar": "avatar3.jpg", "is_admin": False},
                {"id": 5, "username": "luc_photographe", "email": "luc.photographe@example.com", "password_hash": "Password123",
                "bio": "Photographe de rue, capturant la vie quotidienne.", "avatar": "avatar4.jpg", "is_admin": False},
                {"id": 6, "username": "emma_create", "email": "emma.create@example.com", "password_hash": "Password123",
                "bio": "Artiste numérique, j'explore les univers fantastiques.", "avatar": "avatar5.jpg", "is_admin": False},
                {"id": 7, "username": "paul_peinture", "email": "paul.peinture@example.com", "password_hash": "Password123",
                "bio": "Peintre abstrait, mes œuvres expriment le chaos intérieur.", "avatar": "avatar6.jpg", "is_admin": False},
                {"id": 8, "username": "clara_vision", "email": "clara.vision@example.com", "password_hash": "Password123",
                "bio": "Aquarelliste, j'aime les paysages doux et apaisants.", "avatar": "avatar7.jpg", "is_admin": False},
                {"id": 9, "username": "nico_sculpt", "email": "nico.sculpt@example.com", "password_hash": "Password123",
                "bio": "Sculpteur sur bois, inspiré par les traditions anciennes.", "avatar": "avatar8.jpg", "is_admin": False},
                {"id": 10, "username": "lea_graphiste", "email": "lea.graphiste@example.com", "password_hash": "Password123",
                "bio": "Graphiste et illustratrice, fan de couleurs vives.", "avatar": "avatar9.jpg", "is_admin": False}
            ]

            from werkzeug.security import generate_password_hash
            for user_data in users:
                user = User(id=user_data["id"], username=user_data["username"], email=user_data["email"],
                            password_hash=generate_password_hash(user_data["password_hash"]), bio=user_data["bio"],
                            avatar=user_data["avatar"], is_admin=user_data["is_admin"])
                db.session.add(user)

            # Table Emotion
            emotions = [
                {"id": 1, "name": "Joie"},
                {"id": 2, "name": "Tristesse"},
                {"id": 3, "name": "Colère"},
                {"id": 4, "name": "Peur"},
                {"id": 5, "name": "Surprise"},
                {"id": 6, "name": "Dégoût"}
            ]

            for emotion_data in emotions:
                emotion = Emotion(id=emotion_data["id"], name=emotion_data["name"])
                db.session.add(emotion)

            # Table Artwork
            artworks = [
                {"id": 1, "title": "La Joconde", "description": "La Joconde (ou Mona Lisa) de Léonard de Vinci est bien plus qu’un simple portrait: c’est une énigme peinte à l’huile, un silence suspendu entre deux mondes. Dans le clair-obscur subtil de cette toile, le regard de la jeune femme semble suivre le spectateur, oscillant entre douceur et mystère. Son célèbre sourire, imperceptible et fuyant, devient le symbole de ce que l’on ne peut jamais totalement saisir chez l’autre. Le paysage flou derrière elle, irréel et onirique, contraste avec la netteté de son visage, suggérant une tension entre l’humain et l’inconnu, entre la réalité et le rêve.", "image_path": "Joconde.jpg", "emotion_target": "Surprise", "emotion_detected": "neutral", "user_id": 2, "created_at": "2025-05-12 13:32:49.623430"},
                {"id": 2, "title": "La Nuit étoilée", "description": "La Nuit étoilée de Vincent van Gogh est une explosion tourmentée de lumière dans un ciel déchiré. Les étoiles tourbillonnent comme des pensées en fièvre, les nuages ondulent dans un mouvement presque vivant, tandis que le cyprès s’élève, sombre et menaçant, comme une flamme noire entre la terre et le ciel. Le village endormi, paisible et figé, contraste avec l’agitation céleste. Ce tableau ne montre pas simplement une nuit : il hurle une solitude cosmique, une prière peinte dans le désespoir et la beauté. C’est une vision intérieure du monde extérieur, un paysage psychique.", "image_path": "nuit_etoilee.jpg", "emotion_target": "Tristesse", "emotion_detected": "neutral", "user_id": 2, "created_at": "2025-05-12 13:40:10.693791"},
                {"id": 3, "title": "Le Cri", "description": "Le Cri d’Edvard Munch est un hurlement visuel, une onde de choc émotionnelle figée sur toile. La silhouette centrale, au visage distordu, bouche grande ouverte, incarne l’angoisse pure, comme si le monde autour d’elle s’effondrait. Le ciel rougeoyant, les lignes ondulantes du paysage, et le pont qui semble s’effacer sous ses pieds traduisent un univers instable, déformé par la peur et la panique. Tout est vacillant, tout vibre de cette tension existentielle. Ce n’est pas un cri que l’on entend, mais un cri que l’on ressent, un cri intérieur partagé avec violence au monde entier.", "image_path": "le_cris.jpg", "emotion_target": "Peur", "emotion_detected": "anger", "user_id": 2, "created_at": "2025-05-12 13:41:34.744382"},
                {"id": 4, "title": "Guernica", "description": "Guernica de Pablo Picasso est un cri de douleur collective, une fresque monumentale du chaos et de l’inhumanité. En noir, blanc et gris, la scène se tord sous la violence : une femme hurle en tenant son enfant mort, un cheval éventré se cabre, un taureau impassible observe le carnage, et des corps disloqués jonchent l’espace comme autant de fragments d’horreur. Le tableau ne raconte pas une bataille, mais une agonie. Tout y est fracturé, éclaté, comme la mémoire d’un cauchemar lucide. Guernica ne représente pas la guerre — il est la guerre, condensée en douleur brute.", "image_path": "guernica.jpg", "emotion_target": "Colère", "emotion_detected": "anger", "user_id": 2, "created_at": "2025-05-12 13:44:37.715016"},
                {"id": 5, "title": "Les Nymphéas", "description": "Les Nymphéas de Claude Monet sont une immersion dans le silence liquide du temps suspendu. Sur la surface paisible d’un étang, les nénuphars flottent, comme des pensées légères dérivant sans but, portées par une lumière toujours changeante. Il n’y a ni ciel, ni horizon : seulement l’eau, les reflets, et la vibration infinie des couleurs. Les contours s'effacent, la matière devient sensation. C’est un monde sans chaos, sans cris — un refuge. Monet ne peint pas des fleurs, il peint la lumière qui les effleure, le souffle du vent qui les frôle. Une méditation en peinture.", "image_path": "les_nympheas.jpg", "emotion_target": "Joie", "emotion_detected": "neutral", "user_id": 2, "created_at": "2025-05-12 13:46:19.736383"},
                {"id": 6, "title": "La Naissance de Vénus", "description": "La Naissance de Vénus de Sandro Botticelli est une scène mythologique empreinte de grâce et de sensualité divine. La déesse Vénus, surgissant de la mer, incarne la beauté parfaite, une forme idéale, flottant au milieu de vagues douces et d’un ciel lumineux. Ses cheveux dorés semblent danser dans l’air, et son corps, nu, est enveloppé par une conque géante portée par les vagues. À ses côtés, Zéphyr, le vent, souffle doucement, guidant sa naissance vers le rivage, tandis qu’une figure féminine l’accueille avec une cape d'or. Ce tableau, par sa délicatesse et ses proportions harmonieuses, transporte le spectateur dans un monde où l’amour et la beauté se confondent dans une naissance nouvelle.", "image_path": "naissance_de_venus.jpg", "emotion_target": "Joie", "emotion_detected": "neutral", "user_id": 3, "created_at": "2025-05-12 14:00:00.706755"},
                {"id": 7, "title": "Les Ménines", "description": "Les Ménines de Diego Velázquez est un chef-d'œuvre de complexité et de perspective, un jeu subtil entre le regard du spectateur et celui des personnages. Au centre, l'infante Marguerite entourée de ses dames d'honneur (les \"ménines\"), de nains et de chiens, semble capturée dans un instant suspendu. Mais ce qui frappe, c’est la présence de Velázquez lui-même, peintre en pleine action, ajoutant une dimension de mise en abyme. Les miroirs derrière lui reflètent les rois d'Espagne, insinuant que nous, spectateurs, sommes peut-être ceux qui sommes peints. Les hiérarchies sociales sont renversées dans cet espace confiné, l'artiste devenant, lui aussi, une partie de l'élite royale. La scène semble se dérouler entre réalité et illusion, créant un lien intime et étrange avec l’observateur.", "image_path": "les_menines.jpg", "emotion_target": "Surprise", "emotion_detected": "neutral", "user_id": 3, "created_at": "2025-05-12 14:01:15.203018"},
                {"id": 8, "title": "Le Baiser", "description": "Le Baiser de Gustav Klimt est une œuvre d’une sensualité exubérante, un enchevêtrement de corps et d'or qui évoque l’union divine et l'intimité humaine dans une explosion de couleurs et de textures. Les deux figures, enveloppées dans un manteau de motifs dorés et vibrants, sont suspendues dans un moment d’intense communion. Les formes ondulées et les détails décoratifs se fondent dans une symphonie de sensualité et de beauté, tandis que l'étreinte entre les deux amants semble transcender le temps et l’espace. Ce n'est pas seulement un baiser, mais un échange d’âme, un mariage parfait entre le charnel et le spirituel.", "image_path": "le_baiser.jpg", "emotion_target": "Joie", "emotion_detected": "neutral", "user_id": 3, "created_at": "2025-05-12 14:02:35.706490"},
                {"id": 9, "title": "La Persistance de la mémoire", "description": "La Persistance de la mémoire de Salvador Dalí est un tourbillon de perceptions, où le temps lui-même semble se fondre, se déformer et se dissoudre. Les montres molles, pendantes et déformées, flottent comme des souvenirs lointains, distendus par une chaleur irréelle. Le paysage désertique, d’une tranquillité étrange, semble figé dans un état de léthargie, comme si l’espace et le temps étaient devenus malléables, soumis à l’arbitraire de l’imagination. L’éléphant solitaire, aux jambes interminables, et le ciel d’un bleu irréel viennent accentuer ce climat de rêve, où la réalité perd toute sa rigidité. Le tableau suscite une réflexion sur la relativité du temps et la fragilité de la perception humaine.", "image_path": "persistance_de_la_memoire.jpg", "emotion_target": "Peur", "emotion_detected": "neutral", "user_id": 3, "created_at": "2025-05-12 14:04:11.675312"},
                {"id": 10, "title": "La Liberté guidant le peuple", "description": "La Liberté guidant le peuple d’Eugène Delacroix est une vision ardente et héroïque de l’insurrection, où l’allégorie de la Liberté devient une femme vivante, charnelle, déterminée, brandissant le drapeau tricolore dans un élan de fureur et d’espoir. Pieds nus, seins nus, elle avance sur les cadavres, entourée de figures du peuple — bourgeois, ouvriers, enfants — unis par le feu de la révolte. La fumée, les ruines, les armes improvisées composent une scène à la fois chaotique et triomphante. Ce tableau n’est pas seulement une représentation de la révolution de 1830 : c’est un manifeste pictural, un cri collectif pour la justice et la liberté.", "image_path": "La_Liberte_guidant_le_peuple.jpg", "emotion_target": "Colère", "emotion_detected": "anger", "user_id": 3, "created_at": "2025-05-12 14:09:36.606018"},
                {"id": 11, "title": "Le Déjeuner sur l'herbe", "description": "Le Déjeuner sur l’herbe d’Édouard Manet est une scène à la fois paisible et dérangeante, où le banal se teinte d’une étrange tension. Deux hommes en costume discutent, assis dans un sous-bois, tandis qu’une femme nue les accompagne, les regardant frontalement, sans gêne ni soumission. À l’arrière-plan, une autre femme, à demi vêtue, se baigne. Ce mélange de réalisme moderne et de références classiques choque les conventions de l’époque : le nu n’est plus mythologique ni idéalisé, il est contemporain, direct, presque provocant. Ce tableau brise les règles de la peinture académique et interroge le regard du spectateur autant que la place de la femme dans l’espace public.", "image_path": "Le_Dejeuner_sur_lherbe.jpg", "emotion_target": "Dégoût", "emotion_detected": "anger", "user_id": 4, "created_at": "2025-05-12 14:11:27.456622"},
                {"id": 12, "title": "Composition VIII", "description": "Composition VIII de Vassily Kandinsky est une symphonie abstraite où formes géométriques, lignes, cercles et couleurs interagissent dans une danse presque musicale. Ce tableau ne représente rien de concret, et pourtant, il dit tout : le mouvement, le rythme, l’harmonie, le chaos maîtrisé. Chaque élément semble dialoguer avec les autres dans une dynamique mathématique, mais profondément expressive. Kandinsky, influencé par la musique et la spiritualité, compose ici un langage visuel pur, où l’âme se projette à travers les formes. L’espace est structuré, mais jamais figé : c’est un cosmos en expansion, une abstraction vivante.", "image_path": "Composition_VIII.jpg", "emotion_target": "Surprise", "emotion_detected": "neutral", "user_id": 4, "created_at": "2025-05-12 14:12:41.236831"},
                {"id": 13, "title": "Le Penseur", "description": "Le Penseur d’Auguste Rodin est un bloc de tension contenue, une sculpture de bronze où la puissance musculaire se plie à l’intensité de l’esprit. Assis, le corps noué, le menton posé sur le poing, l’homme semble lutter intérieurement, comme si chaque pensée était un combat, chaque idée un poids. Il ne rêve pas, il affronte. Le marbre devient chair, et la chair devient pensée. Ce n’est pas une simple méditation tranquille, c’est une introspection violente, presque douloureuse — l’incarnation du doute, de la conscience, du poids d’exister et de devoir choisir.", "image_path": "Le_Penseur.jpg", "emotion_target": "Tristesse", "emotion_detected": "anger", "user_id": 4, "created_at": "2025-05-12 14:14:06.429237"},
                {"id": 14, "title": "Autoportrait à l'oreille bandée", "description": "Autoportrait à l’oreille bandée de Vincent van Gogh est un miroir brut de la souffrance, un témoignage silencieux d’un esprit au bord de la rupture. Le peintre se montre de profil, le visage pâle et fermé, emmitouflé dans un manteau d’hiver, l’oreille droite couverte de bandages après le fameux épisode d’automutilation. Derrière lui, le chevalet et une estampe japonaise — une référence à l’art qu’il admirait — contrastent avec la gravité de son expression. Ce portrait n’est pas une plainte, mais une lucidité crue : Van Gogh ne cherche pas à susciter la pitié, il s’observe, il s’expose dans un moment de fragilité humaine extrême.", "image_path": "Autoportrait_a_loreille_bande.jpg", "emotion_target": "Tristesse", "emotion_detected": "anger", "user_id": 4, "created_at": "2025-05-12 14:15:11.812029"},
                {"id": 15, "title": "Les Demoiselles d'Avignon", "description": "Les Demoiselles d’Avignon de Pablo Picasso est un choc visuel, une rupture violente avec toute tradition picturale. Cinq figures féminines nues, aux formes anguleuses et aux visages masqués par des influences africaines et ibériques, se dressent dans un espace déstructuré, comme figées dans une danse étrangère à toute harmonie classique. Le spectateur est confronté, frontalement, sans médiation, à des corps disloqués, presque menaçants. Ici, la sensualité devient tension, la beauté devient étrangeté. Picasso ne peint pas des femmes, il fracture la perception, brise le regard académique, et propose une nouvelle grammaire de la forme : brutale, libre, iconoclaste.", "image_path": "Les_Demoiselles_dAvignon.jpg", "emotion_target": "Dégoût", "emotion_detected": "anger", "user_id": 4, "created_at": "2025-05-12 14:17:02.866208"},
                {"id": 16, "title": "La Danse d’Henri Matisse", "description": "La Danse d’Henri Matisse est un tourbillon de vie, une célébration primitive et joyeuse du mouvement. Cinq corps nus, rouges comme la pulsation du sang, tournent en ronde sur un fond de vert et de bleu vibrant. Les formes sont simples, presque enfantines, mais puissantes : elles transcendent la représentation pour capturer l’essence du geste, de la liberté et de l’union. Rien n’est figé, tout est rythme et abandon. Matisse ne cherche pas à illustrer une scène, il donne à voir une émotion pure, une énergie organique et collective. C’est la vie réduite à son élan le plus fondamental : danser, ensemble, hors du temps.\r\n", "image_path": "La_Danse_dHenri_Matisse.jpg", "emotion_target": "Joie", "emotion_detected": "neutral", "user_id": 5, "created_at": "2025-05-12 14:19:58.959286"},
                {"id": 17, "title": "Le Radeau de la Méduse", "description": "Le Radeau de la Méduse de Théodore Géricault est un cri monumental figé dans le bois et la toile, un naufrage autant physique que moral. Sur un radeau de fortune, des survivants désespérés luttent contre la mer et la mort, entassés, à moitié nus, certains déjà morts, d’autres brandissant un espoir fragile vers l’horizon. Ce n’est pas un tableau d’histoire, c’est une dénonciation : celle de l’injustice, de l’abandon, de l’inhumanité d’un pouvoir qui laisse périr ses citoyens. La composition en pyramide, tendue vers un salut incertain, amplifie le drame. C’est une scène de fin du monde — où l’homme n’a plus que lui-même pour survivre, ou pour sombrer.", "image_path": "Le_Radeau_de_la_Meduse.jpg", "emotion_target": "Peur", "emotion_detected": "disgust", "user_id": 5, "created_at": "2025-05-12 14:21:25.010009"},
                {"id": 18, "title": "American Gothic de Grant Wood", "description": "American Gothic de Grant Wood est un portrait iconique de la ruralité américaine, une image figée dans le temps, pleine de rigidité et de caractère. Un homme en costume sombre et une femme, probablement sa fille, se tiennent côte à côte devant une maison de campagne austère, l’expression des deux personnages sévère et intransigeante. Le contraste entre la simplicité des vêtements et la structure du visage, presque sculpturale, dévoile une rigueur morale et une forte résilience, typiques de l’Amérique profonde des années 1930. Le paysage derrière eux est tout aussi sobre : une architecture néogothique qui renforce la sensation de fermeté et de tradition. L'œuvre dépeint à la fois la fierté et la froideur d’une époque, capturant une identité conservatrice et ancrée.", "image_path": "American_Gothic_de_Grant_Wood.jpg", "emotion_target": "Colère", "emotion_detected": "neutral", "user_id": 5, "created_at": "2025-05-12 14:22:33.250210"},
                {"id": 19, "title": "La Grande Vague de Kanagawa", "description": "La Grande Vague de Kanagawa de Katsushika Hokusai est une œuvre saisissante qui capture la puissance indomptable de la mer. La vague géante, avec ses crêtes courbées comme des griffes, semble prête à engloutir les petits bateaux et tout ce qui se trouve sur son chemin. En arrière-plan, le mont Fuji, majestueux et serein, contraste avec la violence de l’océan, représentant à la fois la fragilité de l'homme face à la nature et la permanence de celle-ci. La composition dynamique et les lignes fluides créent un sentiment de mouvement, presque une danse entre la mer et la montagne, entre le chaos et la stabilité. La couleur bleu profond, presque surnaturelle, intensifie la grandeur de la scène.", "image_path": "La_Grande_Vague_de_Kanagawa.jpg", "emotion_target": "Peur", "emotion_detected": "anger", "user_id": 5, "created_at": "2025-05-12 14:23:13.484788"},
                {"id": 20, "title": "Le Jardin des délices", "description": "Le Jardin des délices de Jérôme Bosch est une vision foisonnante et énigmatique, un triptyque hallucinant où l’humanité se perd entre innocence, luxure et damnation. À gauche, le paradis : Dieu présente Ève à Adam dans une nature idyllique mais déjà étrange, pleine d’animaux hybrides et d’architectures organiques. Au centre, un immense jardin grouille de corps nus qui se livrent à tous les plaisirs sensuels imaginables, dans une ambiance à la fois joyeuse et inquiétante. Puis, à droite, l’enfer s’ouvre — sombre, mécanique, peuplé d’instruments de torture, de figures grotesques, de musiciens damnés. C’est une plongée dans l’âme humaine, où le désir devient excès, puis châtiment.", "image_path": "Le_Jardin_des_delices.jpg", "emotion_target": "Dégoût", "emotion_detected": "disgust", "user_id": 5, "created_at": "2025-05-12 14:24:15.519994"},
                {"id": 21, "title": "L'Homme de Vitruve", "description": "L’Homme de Vitruve de Léonard de Vinci est bien plus qu’un simple dessin anatomique : c’est une déclaration philosophique et humaniste sur l’harmonie entre l’homme et l’univers. L’homme y est représenté nu, inscrit à la fois dans un cercle — symbole du divin, de la perfection — et dans un carré — symbole de la terre, du rationnel. Bras et jambes écartés dans deux positions superposées, il devient le centre absolu de toute proportion, l’unité de mesure de toutes choses. Ce schéma illustre la conviction de la Renaissance que l’être humain, par la raison et la science, peut comprendre, ordonner, et même refléter l’ordre du cosmos.", "image_path": "LHomme_de_Vitruve.jpg", "emotion_target": "Surprise", "emotion_detected": "neutral", "user_id": 6, "created_at": "2025-05-12 14:29:32.426144"},
                {"id": 22, "title": "La Laitière", "description": "La Laitière de Johannes Vermeer est un hymne à la simplicité silencieuse, à la beauté des gestes quotidiens. Une femme verse du lait avec une concentration paisible, baignée par une lumière douce qui filtre par une fenêtre invisible. Le calme de la scène, la justesse des couleurs, la texture du pain, la céramique, la robe usée — tout respire l’humilité d’une vie laborieuse, mais digne. Ce tableau n’illustre pas un événement : il célèbre l’instant, la présence, la routine élevée au rang de poésie. Vermeer transforme un geste domestique en acte sacré, où le silence devient langage et la lumière, révélation.", "image_path": "La_Laitiere.jpg", "emotion_target": "Joie", "emotion_detected": "neutral", "user_id": 6, "created_at": "2025-05-12 14:31:26.176126"},
                {"id": 23, "title": "Les Tournesols", "description": "Les Tournesols de Vincent van Gogh sont bien plus que de simples natures mortes florales : ce sont des portraits d’âmes en feu, une ode à la lumière, à la vie, à la matière. Les jaunes éclatants, tantôt vibrants, tantôt ternes, dépeignent différentes étapes de la floraison et de la fanaison, comme une méditation sur le temps qui passe. Les fleurs semblent se tordre, se pencher, s’ouvrir ou mourir avec une intensité presque humaine. Van Gogh ne cherche pas la perfection botanique, mais la vérité émotionnelle. Chaque coup de pinceau épais et tourbillonnant semble animé d’un souffle vital, comme si la peinture elle-même respirait.", "image_path": "Les_Tournesols.jpg", "emotion_target": "Joie", "emotion_detected": "neutral", "user_id": 6, "created_at": "2025-05-12 14:32:51.086027"},
                {"id": 24, "title": "La Trahison des images", "description": "La Trahison des images de René Magritte, avec sa fameuse pipe accompagnée de la phrase « Ceci n’est pas une pipe », est un paradoxe visuel et philosophique qui bouleverse nos certitudes. L’œuvre semble simple, presque banale : une pipe parfaitement dessinée, réaliste, sur fond neutre. Et pourtant, l’inscription en dessous nous oblige à remettre en question notre rapport à la réalité et à la représentation. Ce n’est pas une pipe, car ce n’est qu’une image de pipe — pas un objet réel. Magritte joue avec le langage et la perception pour nous dire que les mots ne sont pas les choses, et que l’image ment autant qu’elle révèle. L'œuvre devient ainsi un piège pour notre esprit logique, une énigme subtile et déstabilisante.", "image_path": "La_Trahison_des_images.jpg", "emotion_target": "Surprise", "emotion_detected": "disgust", "user_id": 6, "created_at": "2025-05-12 14:33:55.532789"},
                {"id": 25, "title": "Olympia", "description": "Olympia d’Édouard Manet est une œuvre de rupture, provocante par sa frontalité et son refus des conventions académiques. Allongée nue sur un lit blanc, une femme nous regarde, droite, assurée, sans détour ni soumission. Ce n’est pas une Vénus idéalisée, mais une courtisane bien réelle, dont le regard nous renvoie à notre propre position de spectateur — complice, client, voyeur ? Sa main posée fermement sur son bas-ventre n’invite pas, elle affirme sa maîtrise. Le contraste entre sa peau pâle et le drap blanc, la présence de la servante noire, la nature morte avec les fleurs : tout évoque la réalité du désir marchandisé, dans une société qui cache ce qu’elle consomme.", "image_path": "Olympia.jpg", "emotion_target": "Dégoût", "emotion_detected": "disgust", "user_id": 6, "created_at": "2025-05-12 14:36:49.452713"}
            ]

            for artwork_data in artworks:
                created_at = datetime.strptime(artwork_data["created_at"], "%Y-%m-%d %H:%M:%S.%f")
                artwork = Artwork(id=artwork_data["id"], title=artwork_data["title"], description=artwork_data["description"],
                                image_path=artwork_data["image_path"], emotion_target=artwork_data["emotion_target"],
                                emotion_detected=artwork_data["emotion_detected"], user_id=artwork_data["user_id"],
                                created_at=created_at)
                db.session.add(artwork)

            # Remplir les tables supplémentaires avec des données plus riches

            # Table Vote (plus de votes avec une répartition variée des émotions)
            votes = [
                # Votes pour l'œuvre 1 (La Joconde - Surprise)
                {"artwork_id": 1, "emotion_id": 5, "user_id": 1},  # Surprise
                {"artwork_id": 1, "emotion_id": 1, "user_id": 3},  # Joie
                {"artwork_id": 1, "emotion_id": 5, "user_id": 4},  # Surprise
                {"artwork_id": 1, "emotion_id": 2, "user_id": 5},  # Tristesse
                {"artwork_id": 1, "emotion_id": 5, "user_id": 6},  # Surprise
                # Votes pour l'œuvre 2 (La Nuit étoilée - Tristesse)
                {"artwork_id": 2, "emotion_id": 2, "user_id": 1},  # Tristesse
                {"artwork_id": 2, "emotion_id": 2, "user_id": 3},  # Tristesse
                {"artwork_id": 2, "emotion_id": 4, "user_id": 4},  # Peur
                {"artwork_id": 2, "emotion_id": 2, "user_id": 5},  # Tristesse
                {"artwork_id": 2, "emotion_id": 1, "user_id": 6},  # Joie
                # Votes pour l'œuvre 3 (Le Cri - Peur)
                {"artwork_id": 3, "emotion_id": 4, "user_id": 1},  # Peur
                {"artwork_id": 3, "emotion_id": 4, "user_id": 4},  # Peur
                {"artwork_id": 3, "emotion_id": 3, "user_id": 5},  # Colère
                {"artwork_id": 3, "emotion_id": 4, "user_id": 6},  # Peur
                {"artwork_id": 3, "emotion_id": 6, "user_id": 7},  # Dégoût
                # Votes pour l'œuvre 4 (Guernica - Colère)
                {"artwork_id": 4, "emotion_id": 3, "user_id": 1},  # Colère
                {"artwork_id": 4, "emotion_id": 3, "user_id": 3},  # Colère
                {"artwork_id": 4, "emotion_id": 4, "user_id": 5},  # Peur
                {"artwork_id": 4, "emotion_id": 3, "user_id": 6},  # Colère
                {"artwork_id": 4, "emotion_id": 6, "user_id": 7},  # Dégoût
                # Votes pour l'œuvre 5 (Les Nymphéas - Joie)
                {"artwork_id": 5, "emotion_id": 1, "user_id": 1},  # Joie
                {"artwork_id": 5, "emotion_id": 1, "user_id": 3},  # Joie
                {"artwork_id": 5, "emotion_id": 1, "user_id": 4},  # Joie
                {"artwork_id": 5, "emotion_id": 2, "user_id": 6},  # Tristesse
                {"artwork_id": 5, "emotion_id": 1, "user_id": 7},  # Joie
                # Votes pour d'autres œuvres (exemple pour quelques œuvres supplémentaires)
                {"artwork_id": 6, "emotion_id": 1, "user_id": 1},  # Joie
                {"artwork_id": 6, "emotion_id": 1, "user_id": 2},  # Joie
                {"artwork_id": 7, "emotion_id": 5, "user_id": 2},  # Surprise
                {"artwork_id": 8, "emotion_id": 1, "user_id": 1},  # Joie
                {"artwork_id": 9, "emotion_id": 4, "user_id": 1},  # Peur
                {"artwork_id": 10, "emotion_id": 3, "user_id": 1},  # Colère
                {"artwork_id": 11, "emotion_id": 6, "user_id": 1},  # Dégoût
                {"artwork_id": 12, "emotion_id": 5, "user_id": 1},  # Surprise
                {"artwork_id": 13, "emotion_id": 2, "user_id": 1},  # Tristesse
                {"artwork_id": 14, "emotion_id": 2, "user_id": 1},  # Tristesse
                {"artwork_id": 15, "emotion_id": 6, "user_id": 1},  # Dégoût
                {"artwork_id": 16, "emotion_id": 1, "user_id": 1},  # Joie
                {"artwork_id": 17, "emotion_id": 4, "user_id": 1},  # Peur
                {"artwork_id": 18, "emotion_id": 3, "user_id": 1},  # Colère
                {"artwork_id": 19, "emotion_id": 4, "user_id": 1},  # Peur
                {"artwork_id": 20, "emotion_id": 6, "user_id": 1},  # Dégoût
                {"artwork_id": 21, "emotion_id": 5, "user_id": 1},  # Surprise
                {"artwork_id": 22, "emotion_id": 1, "user_id": 1},  # Joie
                {"artwork_id": 23, "emotion_id": 1, "user_id": 1},  # Joie
                {"artwork_id": 24, "emotion_id": 5, "user_id": 1},  # Surprise
                {"artwork_id": 25, "emotion_id": 6, "user_id": 1},  # Dégoût
            ]
            for vote_data in votes:
                vote = Vote(artwork_id=vote_data["artwork_id"], emotion_id=vote_data["emotion_id"], user_id=vote_data["user_id"])
                db.session.add(vote)

            # Table Comment (plus de commentaires sur les œuvres)
            comments = [
                {"content": "Magnifique travail, très émouvant!", "artwork_id": 1, "user_id": 3},
                {"content": "Les couleurs sont sublimes!", "artwork_id": 2, "user_id": 4},
                {"content": "Un chef-d'œuvre intemporel.", "artwork_id": 3, "user_id": 5},
                {"content": "J'adore l'énergie de cette œuvre!", "artwork_id": 4, "user_id": 6},
                {"content": "Très paisible, une vraie méditation.", "artwork_id": 5, "user_id": 7},
                {"content": "La composition est incroyable.", "artwork_id": 6, "user_id": 8},
                {"content": "Un peu perturbant mais fascinant.", "artwork_id": 9, "user_id": 9},
                {"content": "Quel sens du détail!", "artwork_id": 10, "user_id": 10},
                {"content": "Une œuvre qui interpelle.", "artwork_id": 11, "user_id": 1},
                {"content": "Les formes sont hypnotiques.", "artwork_id": 12, "user_id": 2},
                {"content": "Cette œuvre me touche profondément.", "artwork_id": 1, "user_id": 4},
                {"content": "Je ressens une immense tristesse en la regardant.", "artwork_id": 2, "user_id": 5},
                {"content": "Quelle puissance dans l'expression!", "artwork_id": 3, "user_id": 6},
                {"content": "Un message fort et poignant.", "artwork_id": 4, "user_id": 7},
                {"content": "Une belle invitation à la sérénité.", "artwork_id": 5, "user_id": 8},
                {"content": "Une œuvre qui déborde de vie!", "artwork_id": 6, "user_id": 9},
                {"content": "Un regard unique sur la réalité.", "artwork_id": 7, "user_id": 10},
                {"content": "Magnifique représentation de l'amour.", "artwork_id": 8, "user_id": 1},
                {"content": "Un voyage dans l'imaginaire!", "artwork_id": 9, "user_id": 2},
                {"content": "Un symbole de liberté impressionnant.", "artwork_id": 10, "user_id": 3},
                {"content": "Une œuvre qui dérange mais qui fait réfléchir.", "artwork_id": 11, "user_id": 4},
                {"content": "Un chef-d'œuvre de l'abstraction.", "artwork_id": 12, "user_id": 5},
                {"content": "Une sculpture qui parle à l'âme.", "artwork_id": 13, "user_id": 6},
                {"content": "Un autoportrait très émouvant.", "artwork_id": 14, "user_id": 7},
                {"content": "Une œuvre audacieuse et provocante.", "artwork_id": 15, "user_id": 8},
                {"content": "Un hymne à la joie et au mouvement!", "artwork_id": 16, "user_id": 9},
                {"content": "Une tragédie capturée avec intensité.", "artwork_id": 17, "user_id": 10},
                {"content": "Une œuvre qui évoque une époque révolue.", "artwork_id": 18, "user_id": 1},
                {"content": "La force de la nature est saisissante.", "artwork_id": 19, "user_id": 2},
                {"content": "Une œuvre complexe et troublante.", "artwork_id": 20, "user_id": 3},
                {"content": "Un dessin d'une précision incroyable.", "artwork_id": 21, "user_id": 4},
                {"content": "Une scène empreinte de douceur.", "artwork_id": 22, "user_id": 5},
                {"content": "Les couleurs vibrantes sont magnifiques!", "artwork_id": 23, "user_id": 6},
                {"content": "Un concept très intéressant!", "artwork_id": 24, "user_id": 7},
                {"content": "Une œuvre qui défie les conventions.", "artwork_id": 25, "user_id": 8},
            ]
            for comment_data in comments:
                comment = Comment(content=comment_data["content"], artwork_id=comment_data["artwork_id"],
                                user_id=comment_data["user_id"])
                db.session.add(comment)

            # Table Report (plus de signalements sur des œuvres et commentaires)
            reports = [
                {"reason": "Contenu inapproprié", "artwork_id": 15, "comment_id": None, "user_id": 7, "created_at": "2025-05-12 14:40:00"},
                {"reason": "Langage offensant", "artwork_id": None, "comment_id": 3, "user_id": 8, "created_at": "2025-05-12 14:41:00"},
                {"reason": "Image choquante", "artwork_id": 20, "comment_id": None, "user_id": 9, "created_at": "2025-05-12 14:42:00"},
                {"reason": "Contenu violent", "artwork_id": 4, "comment_id": None, "user_id": 3, "created_at": "2025-05-12 14:43:00"},
                {"reason": "Commentaire inapproprié", "artwork_id": None, "comment_id": 5, "user_id": 4, "created_at": "2025-05-12 14:44:00"},
                {"reason": "Œuvre dérangeante", "artwork_id": 17, "comment_id": None, "user_id": 5, "created_at": "2025-05-12 14:45:00"},
                {"reason": "Contenu explicite", "artwork_id": 11, "comment_id": None, "user_id": 6, "created_at": "2025-05-12 14:46:00"},
                {"reason": "Langage inapproprié", "artwork_id": None, "comment_id": 10, "user_id": 7, "created_at": "2025-05-12 14:47:00"},
                {"reason": "Image perturbante", "artwork_id": 3, "comment_id": None, "user_id": 8, "created_at": "2025-05-12 14:48:00"},
                {"reason": "Contenu choquant", "artwork_id": 25, "comment_id": None, "user_id": 9, "created_at": "2025-05-12 14:49:00"},
            ]
            for report_data in reports:
                created_at = datetime.strptime(report_data["created_at"], "%Y-%m-%d %H:%M:%S")
                report = Report(reason=report_data["reason"], artwork_id=report_data["artwork_id"],
                                comment_id=report_data["comment_id"], user_id=report_data["user_id"],
                                created_at=created_at)
                db.session.add(report)

            # Table Notification (plus de notifications pour l'admin sur les signalements)
            notifications = [
                {"user_id": 1, "message": "Nouveau signalement sur l'œuvre Les Demoiselles d'Avignon", "created_at": "2025-05-12 14:40:00"},
                {"user_id": 1, "message": "Signalement sur le commentaire de l'œuvre Le Cri", "created_at": "2025-05-12 14:41:00"},
                {"user_id": 1, "message": "Nouveau signalement sur l'œuvre Le Jardin des délices", "created_at": "2025-05-12 14:42:00"},
                {"user_id": 1, "message": "Nouveau signalement sur l'œuvre Guernica", "created_at": "2025-05-12 14:43:00"},
                {"user_id": 1, "message": "Signalement sur le commentaire de l'œuvre Les Nymphéas", "created_at": "2025-05-12 14:44:00"},
                {"user_id": 1, "message": "Nouveau signalement sur l'œuvre Le Radeau de la Méduse", "created_at": "2025-05-12 14:45:00"},
                {"user_id": 1, "message": "Nouveau signalement sur l'œuvre Le Déjeuner sur l'herbe", "created_at": "2025-05-12 14:46:00"},
                {"user_id": 1, "message": "Signalement sur le commentaire de l'œuvre La Liberté guidant le peuple", "created_at": "2025-05-12 14:47:00"},
                {"user_id": 1, "message": "Nouveau signalement sur l'œuvre Le Cri", "created_at": "2025-05-12 14:48:00"},
                {"user_id": 1, "message": "Nouveau signalement sur l'œuvre Olympia", "created_at": "2025-05-12 14:49:00"},
            ]
            for notification_data in notifications:
                created_at = datetime.strptime(notification_data["created_at"], "%Y-%m-%d %H:%M:%S")
                notification = Notification(user_id=notification_data["user_id"], message=notification_data["message"],
                                        created_at=created_at)
                db.session.add(notification)

            # Table Like (inchangé)
            likes = [
                {"user_id": 3, "artwork_id": 1},
                {"user_id": 4, "artwork_id": 2},
                {"user_id": 5, "artwork_id": 3},
                {"user_id": 6, "artwork_id": 4},
                {"user_id": 7, "artwork_id": 5},
                {"user_id": 8, "artwork_id": 6},
                {"user_id": 9, "artwork_id": 9},
                {"user_id": 10, "artwork_id": 10},
                {"user_id": 1, "artwork_id": 11},
                {"user_id": 2, "artwork_id": 12}
            ]
            for like_data in likes:
                like = Like(user_id=like_data["user_id"], artwork_id=like_data["artwork_id"])
                db.session.add(like)

            # Valider les changements
            db.session.commit()
            print("Base de données recréée avec succès !")
        else:
            print("Utilisateurs déjà présents dans la base de données.")
    app.run(debug=True, use_reloader=True, reloader_type='stat')