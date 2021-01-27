# Saagie Community Technologies


[![GitHub release](https://img.shields.io/github/release/saagie/technologies-community?style=for-the-badge)][releases] 
[![GitHub release date](https://img.shields.io/github/release-date/saagie/technologies-community?style=for-the-badge&color=blue)][releases]  


[![Issues](https://img.shields.io/github/issues-raw/saagie/technologies-community?style=for-the-badge&color=blue)][issues]

[![License](https://img.shields.io/github/license/saagie/technologies-community?style=for-the-badge&color=blue)][license]

[![Contributors](https://img.shields.io/github/contributors/saagie/technologies-community?style=for-the-badge&color=blue)][contributors]

[releases]: https://github.com/saagie/technologies-community/releases
[contributors]: https://github.com/saagie/technologies-community/graphs/contributors
[issues]: https://github.com/saagie/technologies-community/issues
[license]: https://github.com/saagie/technologies-community/blob/master/LICENSE


This repository contains all community technologies you can use in Saagie. You can find in [this board](https://github.com/saagie/technologies-community/projects/1) all the technologies that we plan to implement. 

All these technologies shared on this Github repository are supported by its creator or the community on a best effort basis without any obligations. Any bugs found in these technologies will have te be raised through an issue in this repository and won't be covered through Saagie platform SLAs.

Before contributing to this repository, make sure your technology does not already exist in the [Saagie Official Technlogy Repository](https://github.com/saagie/technologies) nor is planned in [the oficial repository kanban](https://github.com/saagie/technologies/projects).


## CONTENTS

This repository contains community job and application technologies.
 
### Job technologies

A job technology can be launched as a job in Saagie. It has :
- a name
- an icon
- some features to create a job
- one or more versions (each can be active/deprecated/inactive for the same technology)

### Application technologies

An application technology can be launch as an application in Saagie. It has : 
- a name
- an icon
- a description
- some default properties to create the application (ports, volumes, ...)


## CONTRIBUTING

All contributions are made with the pull-request system.
Please follow the following steps:

- Create an issue with the correct label (i.e. Documentation/Bug/Feature)
- Create a new branch starting with the issue type : `feature/...`, `bug/...` or `documentation/...`. GitHub Action (CI) will be triggered on each push on your branch. Warning, after the first push on your branch, an automatic commit/push will be made by the CI in order to increment the version. Thus, remember to update your repository after your first commit.
- Implement your new technology into the correct folder : `technologies/[app|job]/technology_name`. This folder should contain :
  - a `metadata.yaml` file which describes your technology, according to the following [documentation](https://docs.saagie.io/developer/latest/sdk/technos/index.html),
  - a `README.md` that contains a quick description, how to build your image and any specific information,
  - a folder with all the mandatory files in order to (re) build the Docker image.
- Open a Pull Request that uses our template (don't forget to link the PR to the issue)
- PR will be reviewed by the Professional Service Team and merged if all the checks are successful
- Tada! Your technology is now part of the community technologies

If you want to check if your image is available, use the following command : `./gradlew checkDockerImages`
To package the technologies in order to test them on Saagie : `./gradlew createZip` (archive will be available in *dist* folder)

### How to create a new technology

You create an issue and a pull-request associated. Refer to [Saagie's official SDK documentation](https://docs.saagie.io/product/latest/sdk/index.html) for more information about how to create a job or a technology.
If you're unsure about the way to contribute to this repository, reach out to service@saagie.com. 
