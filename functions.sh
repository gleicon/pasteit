pasteit_post=http://p.chu.pe/pasteit
pasteit_get=http://p.chu.pe/raw

function xpbcopy() {
  tmp=/tmp/xpbcopy.$$
  trap "rm -f ${tmp}" EXIT
  echo -n "raw=1&codebody=" > $tmp
  IFS=$"\n" cat "${1:-/dev/stdin}" >> $tmp
  if [[ -x `which curl` ]]; then curl --data-binary @${tmp} ${pasteit_post}
  elif [[ -x `which wget` ]]; then wget --post-file=${tmp} -qO- ${pbserver}
  else echo "xpbcopy requires curl or wget"; exit 1; fi
}

function xpbpaste() {
  if [[ -x `which curl` ]]; then curl ${pasteit_get}/$1
  elif [[ -x `which wget` ]]; then wget -qO- ${pbserver}/$1
  else echo "xpbpaste requires curl or wget"; exit 1; fi
}
