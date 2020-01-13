<!DOCTYPE html>
<html>
<head>
	<!-- FONT AWESOME-->
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.11.2/css/all.css" integrity="sha256-46qynGAkLSFpVbEBog43gvNhfrOj+BmwXdxFgVK/Kvc=" crossorigin="anonymous" />

	<!-- FONT PALANQUIN --> 
	<link href="https://fonts.googleapis.com/css?family=Palanquin&display=swap" rel="stylesheet">

	<!-- FRAMEWORK PURE -->
	<link rel="stylesheet" href="https://unpkg.com/purecss@1.0.1/build/pure-min.css" integrity="sha384-oAOxQR6DkCoMliIh8yFnu25d7Eq/PHS21PClpwjOTeU2jRSq11vu66rf90/cZr47" crossorigin="anonymous">
	
	<!-- STYLE CSS --> 
	<link rel="stylesheet" type="text/css" href="style.css">

	<!-- ICONE TAB -->
	<link rel="icon" type="text/css" href="images/icone-easly-dark-transparent-background.png">

	<!-- META -->
	<meta name="viewport" content="width=device-width, user-scalable=no">
	<meta charset="utf-8">
	<meta name="title" content="Easley, le premier Bras Droit digital des entrepreneurs" />
	<meta name="description" content="Basée sur l'intelligence artificielle, Easley gère : gestion financière, pilotage de la trésorerie, maitrise du cash-burn, recommandations etc." />

	<!-- META OG -->
	<meta property="og:title" content="Easley, le premier Bras Droit digital des entrepreneurs">
	<meta property="og:description" content="Basée sur l'intelligence artificielle, Easley gère : gestion financière, pilotage de la trésorerie, maitrise du cash-burn, recommandations etc.">
	<meta property="og:image" content="http://florian-potier-developpeur-web.com/Easley/images/icone-Easley-white.png" />

	<meta name="robots" content= "index, follow">

	<title>Easley, le premier Bras Droit digital des entrepreneurs</title>
</head>
<body>

	<!--
	<aside>
    	<ul class="asideList">
    		<li><a href="" class="asideAnchor">Link</a></li>
      		<li><a href="" class="asideAnchor">Link</a></li>
      		<li><a href="" class="asideAnchor">Link</a></li>
      		<li><a href="" class="asideAnchor">Link</a></li>
    	</ul>
  	</aside>

    	<input type="checkbox" id="myInput">
    	<label for="myInput" id="toHide">
      	<span class="bar top"></span>
      	<span class="bar middle"></span>
      	<span class="bar bottom"></span>
    	</label>
    -->

    <main class="content">
		<header id="header">
			<img id="logo-header" src="images/logo-easly-dark-horizontal.png">
		</header>

		<div id="description-container">
			<h2>En 2020, la Finance, ça sera Easley 🚀</h2>
			<h3>Le premier Bras Droit digital des entrepreneurs</h3>
			<br>
			<div class="items-container">
				<div class="item-box" id="item-box-1">
					<div class="item">
						<i class="fas fa-hand-holding-usd"></i>
					</div>
					<p>Pilotage financier</p>
				</div>

				<div class="item-box" id="item-box-2">
					<div class="item">
						<i class="fas fa-fire-alt"></i>
					</div>
					<p>Maitrise du cash burn</p>
				</div>

				<div class="item-box" id="item-box-3">
					<div class="item">
						<i class="fas fa-chart-pie"></i>
					</div>
					<p>Analyses basées sur vos données</p>
				</div>

				<div class="item-box" id="item-box-4">
					<div class="item">
						<i class="fas fa-robot"></i>
					</div>
					<p>Recommandations qui en découlent</p>
				</div>
			</div>
			<br>
			<p id="texte-description">On est en train d’éduquer notre IA 👩‍🏫, mais elle aura fini l’école et pourra venir vous voir courant 2020 !</p>
		</div>

		<div id="inscription-container">
			<div id="illustration-container">
				<div id="illustration-box">
					<img id="sky" src="images/background.png">
					<img id="fusée" src="images/rocket-147466_1280.png">
					<img id="fire" src="images/fire.png">
					<img class="star" id="star1" src="images/star.png">
				</div>
			</div>
			<div id="inscription-box">

				<?php
					try
					{
						$bdd = new PDO('pgsql:host=ec2-54-75-235-28.eu-west-1.compute.amazonaws.com;dbname=d3t7apg13rcq0r;charset=utf8', 'wdingvfhkjxqwq', 'f320d7d066807877b10ef53914c9ba99d9c9ccf65f84f09a661e7b2685986d8d');
					}
					catch(Exception $e)
					{
					        die('Erreur : '.$e->getMessage());
					}

					$email = isset($_POST['email']) ? $_POST['email'] : NULL;

					if ($email) {
						# email envoyé...
						$bdd->exec("INSERT INTO emails(email) VALUES('$email')");
						?>
							<h2 class="inscription-box-titre">Email bien reçu !</h2>
							<p id="inscription-box-text">On vous tient au courant des avancées du projet !</p>
						<?php
					} 

					else {
						#pas d'email envoyé...
						?>
							<h2 class="inscription-box-titre">Inscrivez-vous !</h2>
							<p id="inscription-box-text">On vous tiendra au courant des avancées du projet !</p>
							<form action="index.php#inscription-box" method="POST" class="formulaire">
							    <input type="email" name="email" id="email" placeholder="Email" required>
							    <input type="submit" value="J'envoie !" class="button-inscription">
							</form>
						<?php
					}
				?>
			</div>
		</div>

		<footer>
			<p>Contactez-nous !</p>
			<p>easley@easleyfin.io</p>
			<p><a href="http://florian-potier-developpeur-web.com" target="_blank" style="opacity: 60%; font-size: 0.8em">Site développé avec <i class="far fa-heart"></i> par Florian Potier</a></p>
		</footer>
	</main>

</body>

<!-- SCRIPT JS --> 
<script type="text/javascript" src="script.js"></script>
<!-- SCRIPT JQUERY --> 
<script src="https://code.jquery.com/jquery-3.4.1.min.js" integrity="sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo=" crossorigin="anonymous"></script>


</html>
