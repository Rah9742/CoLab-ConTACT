@echo off 

set run=python src/main.py
set args=2 Tech Marine Navy AI 

echo Scraping University of Birmingham data
%run% birmingham %args%

echo Scraping University of Manchester data
%run% manchester %args%

echo Scraping University of Portsmouth data
%run% portsmouth %args%

echo Scraping University of Surrey data
%run% surrey %args%

echo Scraping Royal Melbourne Institute of Technology data
%run% rmit %args%

echo Scraping University of Sheffield data
%run% sheffield %args%

echo Scraping University of Leeds data
%run% leeds %args%

echo Scraping University of York data
%run% york %args%

echo Scraping University of West Englang data
%run% uwe %args%

echo Scraping University of lancaster data
%run% lancaster %args%

echo Scraping University of Aberdeen data
%run% aberdeen %args%

echo Scraping University of Bath Spa data
%run% bathspa %args%

echo Scraping University of Exeter data
%run% exeter %args%

echo Scraping University of Wolverhampton data
%run% wolverhampton %args%

echo Scraping Solent University data
%run% solent %args%