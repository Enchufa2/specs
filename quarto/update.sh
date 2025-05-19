#! /usr/bin/bash

set -e

cleanver() { echo $1 | sed -e 's/^v//' -e 's/-.*$//'; }

SPEC=$PWD/*.spec
rm -f *.tar.gz && wget -q $(rpmspec -P $SPEC | grep Source | awk '{print $2}')
TAR=$PWD/*.tar.gz
DIR=$(tar tf $TAR | cut -d"/" -f1 | uniq)
tar xf $TAR
. $DIR/configuration

sed -i '/bundled(/d' $SPEC
sed -i "12i Provides:       bundled(typst)     = $(cleanver $TYPST)" $SPEC
sed -i "12i Provides:       bundled(esbuild)   = $(cleanver $ESBUILD)" $SPEC
sed -i "12i Provides:       bundled(dart-sass) = $(cleanver $DARTSASS)" $SPEC
sed -i "12i Provides:       bundled(pandoc)    = $(cleanver $PANDOC)" $SPEC
sed -i "12i Provides:       bundled(deno-dom)  = $(cleanver $DENO_DOM)" $SPEC
sed -i "12i Provides:       bundled(deno)      = $(cleanver $DENO)" $SPEC

rm -rf $DIR
