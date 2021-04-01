FROM saagie/ttyd-saagie:1.0

#Disable command history (https://github.com/saagie/technologies-community/issues/39)
RUN echo 'set +o history' >> ~/.bashrc

CMD ["ttyd", "bash"]
