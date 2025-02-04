/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * Copyright 2019-2025.
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
pluginManagement {
    repositories {
        mavenLocal()
        gradlePluginPortal()
    }
}
plugins {
    id("com.gradle.develocity") version "3.18"
    id("org.kordamp.gradle.settings") version "0.54.0"
}

apply<org.kordamp.gradle.plugin.settings.SettingsPlugin>()

develocity {
    buildScan {
        termsOfUseUrl = "https://gradle.com/terms-of-service"
        termsOfUseAgree = "yes"
        publishing.onlyIf { false }
    }
}
rootProject.name = "technologies"
val allProjects = mutableListOf<String>()


logger.debug("Start scanning project ...")
File(rootDir.path + "/technologies").walkTopDown().forEach {
    when {
        it.isAGradleModule() -> {
            allProjects.add(relativePath(it.toPath()))
        }
    }
}
configure<org.kordamp.gradle.plugin.settings.ProjectsExtension> {
    setLayout("multi-level")
    enforceNamingConvention.set(false)
    directories.set(allProjects)
}
fun File.isAGradleModule(): Boolean = this.isDirectory && File(this.absolutePath + "/build.gradle.kts").exists()