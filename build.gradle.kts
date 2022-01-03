/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * Copyright 2019 Pierre Leresteux.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     https://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
import com.fasterxml.jackson.databind.ObjectMapper
import com.fasterxml.jackson.module.kotlin.readValue
import com.fasterxml.jackson.module.kotlin.registerKotlinModule
import com.saagie.technologies.SaagieTechnologiesPackageGradlePlugin
import com.saagie.technologies.TYPE
import com.saagie.technologies.modifiedProjects
import net.thauvin.erik.gradle.semver.SemverIncrementBuildMetaTask


val buildDockerTaskName = "buildDockerImage"

plugins {
    id("base")
    id("net.thauvin.erik.gradle.semver") version "1.0.4"
    id("com.bmuschko.docker-remote-api") version "6.1.1"
    id("org.kordamp.gradle.project") version "0.38.0"

}


buildscript {
    repositories {
        mavenLocal()
    }
    dependencies {
        classpath("com.saagie:technologiesplugin:1.2.13")
    }
}
apply<SaagieTechnologiesPackageGradlePlugin>()

config {
    info {
        name = "Technologies Community"
        description = "All Community technologies for Saagie"
        inceptionYear = "2020"
        vendor = "Saagie"

        scm {
            url = "https://github.com/saagie/technologies-community"
        }

        links {
            website = "https://www.saagie.com"
            scm = "https://github.com/saagie/technologies-community"
        }

        licensing {
            licenses {
                license {
                    id = "Apache-2.0"
                }
            }
        }
    }
}

tasks.register("createZip", Zip::class) {
    archiveFileName.set("technologies.zip")
    destinationDirectory.set(file("./dist"))
    from("./technologies") {
        include("**/metadata.yml")
        include("**/metadata.yaml")
    }
}
data class SaagieDockerInfo(val image: String, val version: String)
data class SaagieFinalInnerContexts(val id: String, val dockerInfo: SaagieDockerInfo)
data class SaagieInnerContexts(val id: String, val dockerInfo: SaagieDockerInfo? = null, val innerContexts: List<SaagieFinalInnerContexts>? = null)
data class SaagieContexts(val id: String, val dockerInfo: SaagieDockerInfo, val innerContexts: List<SaagieInnerContexts>? = null)
data class SaagieMetadata(val id: String, val contexts: List<SaagieContexts>)

tasks.register("checkDockerImages") {
    group = "technologies"
    description = "Check if Docker images exist in Docker Hub"

    fun checkImage(image: String, version: String): Unit {
        println("Check if $image:$version is available")
        try {
            java.net.URL("https://hub.docker.com/v2/repositories/$image/tags/$version").readText()
        } catch (e: Exception) {
            throw GradleException("Image or tag $image:$version does not exist in Hub docker")
        }
    }

    doLast {
        var tree: ConfigurableFileTree = fileTree("./technologies") {
            include("**/metadata.yml")
            include("**/metadata.yaml")
        }
        tree.forEach { file: File ->
            val mapper = ObjectMapper(com.fasterxml.jackson.dataformat.yaml.YAMLFactory()).registerKotlinModule()
            mapper.configure(com.fasterxml.jackson.databind.DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false)
            val listing: SaagieMetadata = mapper.readValue(file)
            listing.contexts.forEach {
                checkImage(it.dockerInfo.image, it.dockerInfo.version)
                it.innerContexts?.forEach {
                    if (it.dockerInfo != null) {
                        checkImage(it.dockerInfo.image, it.dockerInfo.version)
                    }
                    it.innerContexts?.forEach {
                        checkImage(it.dockerInfo.image, it.dockerInfo.version)
                    }

                }
            }
        }
    }
}

tasks.register("buildSparkJobs") {
    group = "technologies"
    description = "Build all Spark jobs"
    logger.info(this.description)
    subprojects.forEach {
        dependsOn("${it.path}:$buildDockerTaskName")
    }
}

