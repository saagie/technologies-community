FROM saagie/python:3.6-1.46.0 as python

FROM gus75/vscode_saagie:1.4

ARG PATH_SITES_PACKAGES=/usr/local/lib/python3.6/site-packages
ARG PATH_PYTHON=/usr/local/bin/python
ARG PATH_PIP=/usr/local/bin/pip3.6
ARG PATH_SHARED_LIB=/usr/local/lib/
# ARG PATH_SHARED_LIB_PYTHON="${PATH_SHARED_LIB}libpython3.6m.so.1.0"

COPY --from=python $PATH_SITES_PACKAGES $PATH_SITES_PACKAGES
COPY --from=python $PATH_PYTHON $PATH_PYTHON
COPY --from=python $PATH_PIP $PATH_PIP
COPY --from=python $PATH_SHARED_LIB $PATH_SHARED_LIB

ENV PATH="${PATH}:$PATH_SITES_PACKAGES:$PATH_SHARED_LIB"

RUN chmod -R +x $PATH_SITES_PACKAGES \   
    && chmod -R +x $PATH_PYTHON \
    && chmod -R +x $PATH_PIP \
    && chmod -R +x $PATH_SHARED_LIB

RUN echo $PATH

ENTRYPOINT ["/entrypoint.sh"]