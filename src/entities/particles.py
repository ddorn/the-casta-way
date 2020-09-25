from math import cos, sin

import pygame
from pygame import Vector2 as Vec
from .entity import Entity


class Particle:
    def __init__(self, pos, speed, angle, friction, size, color):
        assert -10 < angle < 10, "This angle is probably not in radians"
        self.pos = Vec(pos)
        self.speed = speed
        self.angle = angle
        self.friction = friction
        self.size = size
        self.color = color

    def logic(self):
        vel = (self.speed * cos(self.angle), self.speed * sin(self.angle))
        self.pos += vel
        self.speed -= self.friction

    def draw(self, display, prop):
        vel = Vec(self.speed * cos(self.angle), self.speed * sin(self.angle))
        display.fill(self.color, (self.pos + vel * prop, (self.size, self.size)))


class ParticleSystem(Entity):
    def __init__(self):
        super(ParticleSystem, self).__init__((0, 0), (1, 1))

        self.particles = set()

    def add(self, particle):
        """Add a particle to the system."""
        self.particles.add(particle)

    def logic(self, game):
        to_remove = set()
        for particle in self.particles:
            particle.logic()

            if particle.speed < 0:
                to_remove.add(particle)

        self.particles.difference_update(to_remove)

    def draw(self, display, prop):
        for particle in self.particles:
            particle.draw(display, prop)
