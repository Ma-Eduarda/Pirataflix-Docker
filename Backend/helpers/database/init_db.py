
from .connection import get_connection
from werkzeug.security import generate_password_hash


def inserir_contas(cur):
    contas = [
        ("Administrador", "admin@gmail.com", "senha123", "adm"),
        ("Usuário", "usuario@gmail.com", "senha123", "usuario")
    ]

    for nome, email, senha, tabela in contas:
        cur.execute(
            f"SELECT id FROM {tabela} WHERE email = %s",
            (email,)
        )

        if cur.fetchone() is None:
            senha_hash = generate_password_hash(senha)

            cur.execute(
                f"""
                INSERT INTO {tabela} (nome, email, senha_hash)
                VALUES (%s, %s, %s)
                """,
                (nome, email, senha_hash)
            )

            print(f"Conta criada: {email}")


def inserir_filmes(cur):
    filmes = [
        (
            "O Poderoso Chefão",
            "Francis Ford Coppola",
            "1972-03-24",
            "A saga da família Corleone, uma das mais poderosas organizações criminosas de Nova York, liderada por Don Vito Corleone.",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRyPyW0p0Tpiw0jII8h6s233mAcEXuyogbH4tvohYFLFw&s=10",
            ["Drama", "Crime"]
        ),
        (
            "Interestelar",
            "Christopher Nolan",
            "2014-11-07",
            "Em um futuro em que a Terra enfrenta uma crise ambiental, um grupo de astronautas parte em uma missão para encontrar um novo lar para a humanidade.",
            "https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg",
            ["Ficção científica", "Drama", "Aventura"]
        ),
        (
            "Matrix",
            "Lana Wachowski e Lilly Wachowski",
            "1999-03-31",
            "Um programador descobre que a realidade em que vive é uma simulação criada por máquinas e se junta a uma resistência humana.",
            "https://image.tmdb.org/t/p/w500/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg",
            ["Ficção científica", "Ação"]
        ),
        (
            "O Cavaleiro das Trevas",
            "Christopher Nolan",
            "2008-07-18",
            "Batman enfrenta o Coringa, um criminoso que espalha o caos por Gotham City e desafia os limites do herói.",
            "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
            ["Ação", "Drama", "Crime"]
        ),
        (
            "Pulp Fiction: Tempo de Violência",
            "Quentin Tarantino",
            "1994-10-14",
            "Histórias interligadas de criminosos, assaltantes e pessoas comuns se cruzam em Los Angeles.",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRDiGDkMdFk6q5ZVvCDO20JPgCmgsStmErAXASuEIroRg&s=10",
            ["Crime", "Drama", "Suspense"]
        ),
        (
            "De Volta para o Futuro",
            "Robert Zemeckis",
            "1985-07-03",
            "Marty McFly viaja acidentalmente ao passado em uma máquina do tempo criada pelo cientista Doc Brown.",
            "https://image.tmdb.org/t/p/w500/fNOH9f1aA7XRTzl1sAOx9iF553Q.jpg",
            ["Ficção científica", "Aventura", "Comédia"]
        ),
        (
            "Forrest Gump: O Contador de Histórias",
            "Robert Zemeckis",
            "1994-07-06",
            "Acompanhe a vida extraordinária de Forrest Gump, um homem que presencia e participa de importantes acontecimentos históricos.",
            "https://image.tmdb.org/t/p/w500/arw2vcBveWOVZr6pxd9XTd1TdQa.jpg",
            ["Drama", "Romance"]
        ),
        (
            "O Rei Leão",
            "Roger Allers e Rob Minkoff",
            "1994-06-24",
            "Simba, um jovem leão, precisa superar a perda de seu pai e enfrentar seu passado para assumir seu lugar como rei.",
            "https://image.tmdb.org/t/p/w500/sKCr78MXSLixwmZ8DyJLrpMsd15.jpg",
            ["Animação", "Aventura", "Drama"]
        ),
        (
            "Jurassic Park: O Parque dos Dinossauros",
            "Steven Spielberg",
            "1993-06-11",
            "Um parque temático com dinossauros clonados se transforma em um lugar perigoso quando os animais escapam do controle.",
            "https://image.tmdb.org/t/p/w500/oU7Oq2kFAAlGqbU4VoAE36g4hoI.jpg",
            ["Aventura", "Ficção científica", "Suspense"]
        ),
        (
            "Titanic",
            "James Cameron",
            "1997-12-19",
            "Durante a viagem inaugural do Titanic, Jack e Rose vivem uma história de amor marcada pela tragédia do navio.",
            "https://image.tmdb.org/t/p/w500/9xjZS2rlVxm8SFx8kPC3aIGCOYQ.jpg",
            ["Romance", "Drama"]
        )
    ]

    for titulo, diretor, data, sinopse, capa, generos in filmes:
        cur.execute(
            "SELECT id FROM filme WHERE titulo = %s",
            (titulo,)
        )

        resultado = cur.fetchone()

        if resultado is None:
            cur.execute(
                """
                INSERT INTO filme
                    (titulo, diretor, dt_lancamento, sinopse, capa_filme)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
                """,
                (titulo, diretor, data, sinopse, capa)
            )

            filme_id = cur.fetchone()[0]
            print(f"Filme cadastrado: {titulo}")
        else:
            filme_id = resultado[0]

        for genero in generos:
            cur.execute(
                """
                SELECT id FROM filme_genero
                WHERE filme_id = %s AND genero_nome = %s
                """,
                (filme_id, genero)
            )

            if cur.fetchone() is None:
                cur.execute(
                    """
                    INSERT INTO filme_genero (filme_id, genero_nome)
                    VALUES (%s, %s)
                    """,
                    (filme_id, genero)
                )


def init_database():
    conn = get_connection()
    cur = conn.cursor()

    with open("helpers/database/schema.sql", "r", encoding="utf-8") as f:
        sql_script = f.read()

    cur.execute(sql_script)

    cur.execute(
        "ALTER TABLE filme ADD COLUMN IF NOT EXISTS sinopse TEXT"
    )

    cur.execute("""
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1
                FROM information_schema.columns
                WHERE table_schema = current_schema()
                  AND table_name = 'filme'
                  AND column_name = 'roteiro'
            ) THEN
                EXECUTE 'UPDATE filme SET sinopse = COALESCE(sinopse, roteiro)';
            END IF;
        END $$;
    """)

    inserir_contas(cur)
    inserir_filmes(cur)

    conn.commit()
    cur.close()
    conn.close()

    print("Banco inicializado com sucesso.")
