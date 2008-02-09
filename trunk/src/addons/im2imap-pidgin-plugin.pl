use Purple;

%PLUGIN_INFO = (
    perl_api_version => 2,
    name => "im2imap-Integration",
    version => "0.1",
    summary => "Plugin for im2imap",
    description => "plugin calls im2imap every time pidgin is started",
    author => "Sebastian Moors <sebastian.moors\@gmail.com>",
    url => "http://im2imap.berlios.de",

    load => "plugin_load",
    unload => "plugin_unload"
);

sub plugin_init {
    return %PLUGIN_INFO;
}

sub plugin_load {
    my $plugin = shift;
    Purple::Debug::info("testplugin", "plugin_load() - Test Plugin Loaded.\n");
}

sub plugin_unload {
    my $plugin = shift;
    system('im2imap -c pidgin');
    Purple::Debug::info("testplugin", "plugin_unload() - Test Plugin Unloaded.\n");
}


