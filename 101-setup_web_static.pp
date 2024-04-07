# sets up your web servers for the deployment of web_static

package {'nginx':
  ensure => installed,
}

$dirs = [
  '/data/',
  '/data/web_static/',
  '/data/web_static/releases/',
  '/data/web_static/shared/',
  '/data/web_static/releases/test/',
  ]

$dirs.each | String $dir | {
  file {$dir:
    ensure => directory,
  }
}

file {'/data/web_static/releases/test/index.html':
  ensure  => file,
  content => 'Nginx installed successfully!',
}

file {'link':
  ensure  => link,
  path    => '/data/web_static/current',
  target  => '/data/web_static/releases/test/',
  require => File['/data/web_static/releases/test/'],
}

exec {'set ownership':
  command => '/bin/chown --recursive --no-dereference ubuntu:ubuntu /data/',
  require => File['/data/'],
}

$line_str = '    location /hbnb_static {
        alias /data/web_static/current/;
    }'
file_line {'serve content':
  ensure  => present,
  path    => '/etc/nginx/sites-available/default',
  match   => '    location /hbnb_static {',
  line    => $line_str,
  after   => '    root /var/www/html;',
  replace => false,
}

service {'nginx':
  ensure => running,
}
