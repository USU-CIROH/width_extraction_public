# width_extraction_public
 




<!-- ABOUT THE PROJECT -->
## Width Extraction toolset



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

* arcpy
* numpy
* pandas


<!-- USAGE EXAMPLES -->
## Usage

#### main.py

* Input
 - XS lines (path_xsect): path to the transect lines (e.g., './gis_files/thalweg_XS_20m_200m.shp' where station interval = 20 m, length = 200 m)
 - Terrains (path_terrains): path to the terraian (XX.asc), can process two terrains as of now (e.g., ['./DEM/pre-fire.tif', './DEM/post-fire.tif'])
  
* Output
 - Figures of XS profiles of multiple terrains in 'figures' folder 
<p align="center" width="100%">
<img width="50%" src="/figures/xsect_20m_200m_1p25m_same_vertical_offset/profile_186.png" alt="output0">
</p>

 - Figures of longitudinal bed elevation and width series in 'figures' folder
  - Bed elevation
<p align="center" width="100%">
<img width="50%" src="/figures/z_series_20m_200m_1p25m_same_vertical_offset.png" alt="output1">
</p>
  - Bed elevation
<p align="center" width="100%">
<img width="50%" src="/figures/w_series_20m_200m_1p25m_same_vertical_offset.png" alt="output2">
</p>
  - Table of longitudinal bed elevation and width series in 'tables' folder




<!-- ROADMAP 

## Roadmap

- [x] Add Changelog
- [x] Add back to top links
- [ ] Add Additional Templates w/ Examples
- [ ] Add "components" document to easily copy & paste sections of the readme
- [ ] Multi-language Support
    - [ ] Chinese
    - [ ] Spanish
-->


<!-- CONTRIBUTING 
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
-->

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.



<!-- CONTACT -->
## Contact

Anzy Lee anzy.lee@usu.edu

Project Link: [https://github.com/anzylee/HAND-FIM_Assessment_public](https://github.com/anzylee/HAND-FIM_Assessment_public)


<!-- ACKNOWLEDGMENTS 
## Acknowledgments

Use this space to list resources you find helpful and would like to give credit to. I've included a few of my favorites to kick things off!

* [Choose an Open Source License](https://choosealicense.com)
* [GitHub Emoji Cheat Sheet](https://www.webpagefx.com/tools/emoji-cheat-sheet)
* [Malven's Flexbox Cheatsheet](https://flexbox.malven.co/)
* [Malven's Grid Cheatsheet](https://grid.malven.co/)
* [Img Shields](https://shields.io)
* [GitHub Pages](https://pages.github.com)
* [Font Awesome](https://fontawesome.com)
* [React Icons](https://react-icons.github.io/react-icons/search)
-->

<p align="right">(<a href="#readme-top">back to top</a>)</p>

