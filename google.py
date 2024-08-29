<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dynamic Google Image Search</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            padding: 20px;
            width: 90%;
            max-width: 600px;
        }
        h1 {
            text-align: center;
            color: #333;
        }
        form {
            display: flex;
            flex-direction: column;
        }
        label {
            margin-bottom: 8px;
            color: #555;
        }
        input[type="text"] {
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            margin-bottom: 15px;
            font-size: 16px;
        }
        button {
            background-color: #007bff;
            color: #fff;
            border: none;
            border-radius: 4px;
            padding: 10px 15px;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        button:hover {
            background-color: #0056b3;
        }
        .search-results {
            margin-top: 20px;
            text-align: center;
        }
        .search-results a {
            text-decoration: none;
        }
        .search-results button {
            background-color: #28a745;
            color: #fff;
        }
        .search-results button:hover {
            background-color: #218838;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Generate a Google Image Search</h1>
        <form id="searchForm">
            <label for="theme">Theme:</label>
            <input type="text" id="theme" name="theme" placeholder="e.g., Modern">

            <label for="industry">Industry:</label>
            <input type="text" id="industry" name="industry" placeholder="e.g., Education">

            <label for="designs">Design Keywords:</label>
            <input type="text" id="designs" name="designs" placeholder="e.g., Minimalist, Responsive">

            <button type="button" onclick="generateImageSearch()">Search Images</button>
        </form>

        <div id="searchLink" class="search-results"></div>
    </div>

    <script>
        function generateImageSearch() {
            // Get values from the input fields
            var theme = document.getElementById('theme').value;
            var industry = document.getElementById('industry').value;
            var designs = document.getElementById('designs').value;

            // List of top design websites to search
            var sites = [
                'behance.net',       // Behance
                'dribbble.com',      // Dribbble
                'awwwards.com',      // Awwwards
                'designinspiration.com', // Design Inspiration
                'siteinspire.com',   // SiteInspire
                'cssdesignawards.com', // CSS Design Awards
                'webdesignerdepot.com', // Web Designer Depot
                'smashingmagazine.com', // Smashing Magazine
                'creativemarket.com', // Creative Market
                'flickr.com'         // Flickr (for additional design inspiration)
            ];

            // Create the site filter part of the query
            var siteFilter = sites.map(site => `site:${site}`).join(' OR ');

            // Construct the query
            var query = `${theme} ${industry} website design ${designs} ${siteFilter}`;

            // Encode the query for use in a URL
            var encodedQuery = encodeURIComponent(query);

            // Construct the Google Images search URL
            var searchUrl = `https://www.google.com/search?hl=en&tbm=isch&q=${encodedQuery}`;

            // Display the search link
            var linkElement = document.getElementById('searchLink');
            linkElement.innerHTML = `
                <p>Click the button below to view images related to:</p>
                <p><strong>${query}</strong></p>
                <a href="${searchUrl}" target="_blank">
                    <button>Search Images</button>
                </a>
            `;
        }
    </script>
</body>
</html>
